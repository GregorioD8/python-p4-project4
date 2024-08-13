from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource
from datetime import datetime
from models import db, Client, Coach, Session, CoachClient

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
    return 'Welcome to the Coaching App'

class Clients(Resource):
    def get(self):
        try:
            clients = Client.query.all()
            new_clients = [c.to_dict(only=('id', 'name', 'goals')) for c in clients]
            return new_clients, 200
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
            return {'errors': ['validation errors', str(e)]}, 400

api.add_resource(Clients, '/clients')

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

api.add_resource(ClientsById, '/clients/<int:id>')

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
                specialization=request.json['specialization']
            )
            db.session.add(new_coach)
            db.session.commit()
            return new_coach.to_dict(only=('id', 'name', 'specialization')), 201
        except Exception as e:
            return {'errors': ['validation errors', str(e)]}, 400

api.add_resource(Coaches, '/coaches')

class CoachesById(Resource):
    def get(self, id):
        try:
            coach = Coach.query.filter_by(id=id).first()
            if not coach:
                return {'error': 'Coach not found'}, 404
            return coach.to_dict(only=('id', 'name', 'specialization', 'clients', 'sessions')), 200
        except Exception as e:
            return {'error': 'Coach not found', 'message': str(e)}, 404

    def patch(self, id):
        try:
            coach = Coach.query.filter_by(id=id).first()
            if not coach:
                return {'error': 'Coach not found'}, 404
            data = request.json
            for key, value in data.items():
                setattr(coach, key, value)
            db.session.commit()
            return coach.to_dict(only=('id', 'name', 'specialization', 'clients', 'sessions')), 200
        except Exception as e:
            return {'errors': ['validation errors', str(e)]}, 400

    def delete(self, id):
        try:
            coach = Coach.query.filter_by(id=id).first()
            if not coach:
                return {'error': 'Coach not found'}, 404
            db.session.delete(coach)
            db.session.commit()
            return {}, 204
        except Exception as e:
            return {'error': 'Coach not found', 'message': str(e)}, 404

api.add_resource(CoachesById, '/coaches/<int:id>')

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
                    'coach': session.coach.to_dict(only=('id', 'name')),
                    'client': session.client.to_dict(only=('id', 'name'))
                }
                for session in sessions
            ]
            return session_data, 200
        except Exception as e:
            return {'error': 'Bad request', 'message': str(e)}, 400

    def post(self):
        try:
            new_session = Session(
                date=datetime.strptime(request.json['date'], '%Y-%m-%d %H:%M:%S'),
                notes=request.json['notes'],
                goal_progress=request.json['goal_progress'],
                coach_id=request.json['coach_id'],
                client_id=request.json['client_id']
            )
            db.session.add(new_session)
            db.session.commit()
            return new_session.to_dict(), 201
        except Exception as e:
            return {'errors': ['validation errors', str(e)]}, 400

api.add_resource(Sessions, '/sessions')

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

api.add_resource(SessionsById, '/sessions/<int:session_id>')

@app.route('/coaches/<int:coach_id>/clients')
def get_clients_for_coach(coach_id):
    try:
        coach_clients = CoachClient.query.filter_by(coach_id=coach_id).all()
        client_list = [cc.client.to_dict(only=('id', 'name')) for cc in coach_clients]
        return jsonify(client_list), 200
    except Exception as e:
        return {'error': 'Bad request', 'message': str(e)}, 400

@app.route('/coaches/<int:coach_id>/sessions')
def get_sessions_for_coach(coach_id):
    try:
        client_id = request.args.get('client_id')
        query = db.session.query(Session, Client, Coach)\
                          .join(Client, Session.client_id == Client.id)\
                          .join(Coach, Session.coach_id == Coach.id)\
                          .filter(Session.coach_id == coach_id)
        
        if client_id:
            query = query.filter(Session.client_id == client_id)
        
        sessions = query.all()
        session_list = [{
            'id': s.Session.id,
            'date': s.Session.date.strftime('%Y-%m-%d %H:%M:%S'),
            'client_name': s.Client.name,
            'coach_name': s.Coach.name,  # Include coach name
            'notes': s.Session.notes,
            'goal_progress': s.Session.goal_progress
        } for s in sessions]
        return jsonify(session_list), 200
    except Exception as e:
        return {'error': 'Bad request', 'message': str(e)}, 400

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

api.add_resource(CoachClientResource, '/coach_clients')

if __name__ == '__main__':
    app.run(debug=True)