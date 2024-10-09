from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from config import db, Config
from models import Client, Coach, Session, CoachClient

# Load environment variables from .env file
load_dotenv('../.env')

# Create and configure Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS
CORS(app)

# Initialize Flask extensions
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(coach_id):
    coach = Coach.query.get(int(coach_id))
    if coach is None:
        print(f"Coach with ID {coach_id} not found")
    return coach

# Register the app with the database
db.init_app(app)

# Instantiate REST API
api = Api(app)

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

# Add the rest of your resource classes here...

# Add resources to the API
api.add_resource(Clients, '/clients')
api.add_resource(Coaches, '/coaches')
api.add_resource(Sessions, '/sessions')
api.add_resource(SessionsById, '/sessions/<int:session_id>')
api.add_resource(CoachClientResource, '/coach_clients')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')