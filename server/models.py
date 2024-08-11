from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from config import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime


convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)

########################################

class Coach(db.Model, SerializerMixin):
    __tablename__ = 'coaches'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    specialization = db.Column(db.String)

    sessions = db.relationship('Session', cascade='all,delete', backref='coach')
    clients = association_proxy('sessions', 'client')

    serialize_rules = ('-sessions.coach',)

    def __repr__(self):
        return f'<Coach {self.id}: {self.name}, specialization: {self.specialization}>'

class Client(db.Model, SerializerMixin):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    goals = db.Column(db.String)

    sessions = db.relationship('Session', cascade='all,delete', backref='client')
    
    serialize_rules = ('-sessions.client',)

    @validates('name')
    def validate_name(self, key, name):
        print('Inside the name validation')
        if not name or len(name) < 1:
            raise ValueError('Name must exist')
        return name
    
    @validates('goals')
    def validate_goals(self, key, goals):
        print('Inside the goals validation')
        if not goals or len(goals) < 1:
            raise ValueError('must enter a goal')
        return goals
    
    def __repr__(self):
        return f'<Client {self.id}: {self.name}, field: {self.goals}>'

class Session(db.Model, SerializerMixin):
    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.String)
    goal_progress = db.Column(db.Integer)

    coach_id = db.Column(db.Integer, db.ForeignKey('coaches.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)

    serialize_rules = ('-client.sessions', '-coach.sessions')
    
    @validates('date')
    def validate_date(self, key, date):
        print('Inside the date validation')
        if not date:
            raise ValueError('Date must exist')
        return date

    @validates('client_id')
    def validate_client_id(self, key, client_id):
        print('Inside the client_id validation')
        if not client_id:
            raise ValueError('must enter a client_id')
        return client_id
    
    @validates('coach_id')
    def validate_coach_id(self, key, coach_id):
        print('Inside the coach_id validation')
        if not coach_id:
            raise ValueError('must enter a coach_id')
        return coach_id

    @validates('goal_progress')
    def validate_goal_progress(self, key, goal_progress):
        if not (1 <= goal_progress <= 10):
            raise ValueError('goal_progress must be between 1 and 10')
        return goal_progress

 

    def __repr__(self):
        return f'Session {self.id}: {self.date}, client: {self.client_id}, coach: {self.coach_id}'