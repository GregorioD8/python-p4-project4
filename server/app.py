import os
from dotenv import load_dotenv
import boto3
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from datetime import datetime
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from config import db, app

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '../.env'))

# Fetch secrets from AWS Secrets Manager
def get_secret():
    secret_name = os.getenv('SECRET_NAME')  # Get secret name from .env
    region_name = os.getenv('AWS_REGION')   # Get region name from .env

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)

    try:
        # Fetch secret
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = get_secret_value_response['SecretString']
        secret_dict = json.loads(secret)
    except Exception as e:
        raise e

    return secret_dict

# Fetch secrets from AWS Secrets Manager
secrets = get_secret()

# Configure the app using the secrets fetched from AWS Secrets Manager
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{secrets['username']}:{secrets['password']}@{secrets['host']}:{secrets['port']}/{secrets['dbname']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Fetch and configure secret key from Secrets Manager
app.config['SECRET_KEY'] = secrets.get('secret_key')

# Enable JSON pretty print
app.json.compact = False

# Initialize Migrate
migrate = Migrate(app, db)

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(coach_id):
    return Coach.query.get(int(coach_id))

# Enable CORS
CORS(app)

# Instantiate REST API
api = Api(app)

# Import your models AFTER initializing app, db, etc.
from models import Client, Coach, Session, CoachClient

# Define your resource classes
class Clients(Resource):
    def get(self):
        try:
            clients = Client.query.all()
            client_list = [client.to_dict(only=('id', 'name', 'goals')) for client in clients]
            return client_list, 200
        except Exception as e:
            return {'error': 'Bad request', 'message': str(e)}, 400

    def post(self):
        try:
            new_client = Client(
                name=request.json['name'],
                goals=request.json['goals']
            )
            db.session.add(new_client)
            db.session.commit()
            return new_client.to_dict(only=('id', 'name', 'goals')), 201
        except Exception as e:
            return {'error': str(e)}, 400

class ClientsById(Resource):
    def get(self, id):
        try:
            client = Client.query.filter_by(id=id).first()
            if not client:
                return {'error': 'Client not found'}
            return client.to_dict(only=('id', 'name', 'goals', 'sessions')), 200
        except Exception as e:
            return {'error': 'Client not found', 'message': str(e)}, 404

    def patch(self, id):
        try:
            client = Client.query.filter_by(id=id).first()
            if not client:
                return {'error': 'Client not found'}, 404
            data = request.json
            for key, value in data.items():
                setattr(client, key, value)
            db.session.commit()
            return client.to_dict(only=('id', 'name', 'goals', 'sessions')), 200
        except Exception as e:
            return {'errors': ['validation errors', str(e)]}, 400

    def delete(self, id):
        try:
            client = Client.query.filter_by(id=id).first()
            if not client:
                return {'error': 'Client not found'}
            db.session.delete(client)
            db.session.commit()
            return {}, 204
        except Exception as e:
            return {'error': 'Client not found', 'message': str(e)}, 404

class Coaches(Resource):
    def get(self):
        try:
            coaches = [coach.to_dict(only=('id', 'name', 'specialization')) for coach in Coach.query.all()]
            return coaches, 200
        except Exception as e:
            return {'error': 'Bad request', 'message': str(e)}, 400

    def post(self):
        try:
            new_coach = Coach(
                name=request.json['name'],
                specialization=request.json['specialization'],
                username=request.json['username'],
                password_hash=generate_password_hash(request.json['password'], method='sha256')
            )
            db.session.add(new_coach)
            db.session.commit()
            return new_coach.to_dict(only=('id', 'name', 'specialization', 'username')), 201
        except Exception as e:
            return {'errors': ['validation errors', str(e)]}, 400

class Sessions(Resource):
    def get(self):
        try:
            sessions = Session.query.all()
            session_data = [
                {
                    'id': session.id,
                    'date': session.date.strftime('%Y-%m-%d %H:%M:%S'),
                    'notes': session.notes,
                    'goal_progress': session.goal_progress,
                    'coach_name': session.coach.name,
                    'client_name': session.client.name,
                }
                for session in sessions
            ]
            return session_data, 200
        except Exception as e:
            return {'error': 'Bad request', 'message': str(e)}, 400

    def post(self):
        data = request.json

        try:
            date_str = data.get('date')
            datetime_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')

            new_session = Session(
                date=datetime_obj,
                notes=data['notes'],
                goal_progress=data['goal_progress'],
                coach_id=data['coach_id'],
                client_id=data['client_id']
            )
            db.session.add(new_session)
            db.session.commit()
            return {
                'id': new_session.id,
                'date': new_session.date.strftime('%Y-%m-%d %H:%M:%S'),
                'notes': new_session.notes,
                'goal_progress': new_session.goal_progress,
                'coach_name': new_session.coach.name,
                'client_name': new_session.client.name,
            }, 201
        except Exception as e:
            print("Error when creating a new session:", str(e))
            return {'errors': ['validation errors', str(e)]}, 400

class SessionsById(Resource):
    def patch(self, session_id):
        try:
            session = Session.query.get_or_404(session_id)
            data = request.json
            for key, value in data.items():
                setattr(session, key, value)
            db.session.commit()
            session_data = {
                'id': session.id,
                'date': session.date.strftime('%Y-%m-%d %H:%M:%S'),
                'notes': session.notes,
                'goal_progress': session.goal_progress,
                'coach': session.coach.to_dict(only=('id', 'name')),
                'client': session.client.to_dict(only=('id', 'name'))
            }
            return session_data, 200
        except Exception as e:
            return {'errors': ['validation errors', str(e)]}, 400

    def delete(self, session_id):
        try:
            session = Session.query.get_or_404(session_id)
            db.session.delete(session)
            db.session.commit()
            return {}, 204
        except Exception as e:
            return {'error': 'Session not found', 'message': str(e)}, 404

class CoachClientResource(Resource):
    def get(self):
        try:
            coach_clients = CoachClient.query.all()
            return [cc.to_dict() for cc in coach_clients], 200
        except Exception as e:
            return {'error': 'Bad request', 'message': str(e)}, 400

    def post(self):
        try:
            new_coach_client = CoachClient(
                coach_id=request.json['coach_id'],
                client_id=request.json['client_id'],
                notes=request.json.get('notes', '')
            )
            db.session.add(new_coach_client)
            db.session.commit()
            return new_coach_client.to_dict(), 201
        except Exception as e:
            return {'errors': ['validation errors', str(e)]}, 400

# Add resources to the API
api.add_resource(Clients, '/clients')
api.add_resource(ClientsById, '/clients/<int:id>')
api.add_resource(Coaches, '/coaches')
api.add_resource(Sessions, '/sessions')
api.add_resource(SessionsById, '/sessions/<int:session_id>')
api.add_resource(CoachClientResource, '/coach_clients')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')