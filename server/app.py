from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource
import os
from models import db, Client, Coach, Session
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# Instantiate CORS
CORS(app)
migrate = Migrate(app, db)
db.init_app(app)

# Instantiate REST API
api = Api(app)

@app.route('/')
def home():
    return ''

class Clients(Resource):
    def get(self):
        try:
            clients = Client.query.all()
            new_clients = [c.to_dict(only=('id', 'name', 'goals')) for c in clients]
            return new_clients, 200
        except:
            return {'error': 'Bad request'}, 400

    def post(self):
        try:
            new_client = Client(
                name=request.json['name'],
                goals=request.json['goals']
            )
            db.session.add(new_client)
            db.session.commit()
            return new_client.to_dict(only=('id', 'name', 'goals')), 201
        except:
            return {'errors': ['validation errors']}, 400

api.add_resource(Clients, '/clients')

class ClientsById(Resource):
    def get(self, id):
        try:
            client = Client.query.filter_by(id=id).first()
            if not client:
                return {'error': 'Client not found'}
            return client.to_dict(only=('id', 'name', 'goals', 'sessions')), 200
        except:
            return {'error': 'Client not found'}, 404

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
        except:
            return {'errors': ['validation errors']}, 400

    def delete(self, id):
        try:
            client = Client.query.filter_by(id=id).first()
            if not client:
                return {'error': 'Client not found'}
            db.session.delete(client)
            db.session.commit()
            return {}, 204
        except:
            return {'error': 'Client not found'}, 404

api.add_resource(ClientsById, '/clients/<int:id>')

class Coaches(Resource):
    def get(self):
        try:
            coaches = [coach.to_dict(only=('id', 'name', 'specialization')) for coach in Coach.query.all()]
            return coaches, 200
        except:
            return {'error': 'Bad request'}, 400

api.add_resource(Coaches, '/coaches')

class Sessions(Resource):
    def get(self):
        try:
            sessions = Session.query.all()
            return [session.to_dict() for session in sessions], 200
        except:
            return {'error': 'Bad request'}, 400

    def post(self):
        try:
            session = Session(
                date=datetime.strptime(request.json['date'], '%Y-%m-%d %H:%M:%S'),
                name=request.json['name'],
                client_id=request.json['client_id'],
                coach_id=request.json['coach_id'],
                notes=request.json['notes'],
                goal_progress=request.json['goal_progress']
            )
            db.session.add(session)
            db.session.commit()
            return session.to_dict(), 201
        except:
            return {'errors': ['validation errors']}, 400

api.add_resource(Sessions, '/sessions')

if __name__ == '__main__':
    app.run(port=5000)