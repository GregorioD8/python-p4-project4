from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from config import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)

class Coach(db.Model, SerializerMixin):
    __tablename__ = 'coaches'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    specialization = db.Column(db.String)
    username = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    
    sessions = db.relationship('Session', cascade='all,delete', backref='coach')
    clients = association_proxy('coach_clients', 'client')

    serialize_rules = ('-sessions.coach', '-coach_clients.coach')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

class Client(db.Model, SerializerMixin):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    goals = db.Column(db.String)
    
    sessions = db.relationship('Session', cascade='all,delete', backref='client')
    coaches = association_proxy('coach_clients', 'coach')

    serialize_rules = ('-sessions.client', '-coach_clients.client')

class CoachClient(db.Model, SerializerMixin):
    __tablename__ = 'coach_clients'
    
    id = db.Column(db.Integer, primary_key=True)
    coach_id = db.Column(db.Integer, db.ForeignKey('coaches.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    notes = db.Column(db.String)  
    
    coach = db.relationship('Coach', backref='coach_clients')
    client = db.relationship('Client', backref='coach_clients')

    serialize_rules = ('-coach.coach_clients', '-client.coach_clients')

class Session(db.Model, SerializerMixin):
    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.String)
    goal_progress = db.Column(db.Integer)
    paid_status = db.Column(db.Boolean, default=False)  # Add this line

    coach_id = db.Column(db.Integer, db.ForeignKey('coaches.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)

    serialize_rules = ('-client.sessions', '-coach.sessions')

    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date.strftime('%Y-%m-%d %H:%M:%S'),
            'notes': self.notes,
            'goal_progress': self.goal_progress,
            'paid_status': self.paid_status,  # Add this line
            'coach_id': self.coach_id,
            'client_id': self.client_id,
        }
    
    @validates('date')
    def validate_date(self, key, date):
        if isinstance(date, str):
            try:
                date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            except ValueError as e:
                raise ValueError(f"Date format error: {str(e)}")
        elif not isinstance(date, datetime):
            raise ValueError('Invalid date format. It must be a datetime object or a properly formatted string.')
        return date

    @validates('client_id')
    def validate_client_id(self, key, client_id):
        if not client_id:
            raise ValueError('Client ID must exist')
        return client_id
    
    @validates('coach_id')
    def validate_coach_id(self, key, coach_id):
        if not coach_id:
            raise ValueError('Coach ID must exist')
        return coach_id

    @validates('goal_progress')
    def validate_goal_progress(self, key, goal_progress):
        if not (1 <= goal_progress <= 10):
            raise ValueError('Goal progress must be between 1 and 10')
        return goal_progress

    def __repr__(self):
        return f'Session {self.id}: {self.date}, client: {self.client_id}, coach: {self.coach_id}'