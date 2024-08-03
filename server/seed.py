from app import app
from models import db, Coach, Client, Session
import os
from datetime import datetime

def create_coaches():
    coaches = [
        Coach(name="Matilda Hubert", specialization="Trauma Coaching"),
        Coach(name="Ricky Milton", specialization="Mindfulness and Performance Coaching"),
        Coach(name="Sam Morton", specialization="Depression Coaching"),
        Coach(name="Denise Lawson", specialization="Trauma Coaching"),
        Coach(name="Natalie Ventura", specialization="Mindfulness and Performance Coaching"),
        Coach(name="Veronica Bolton", specialization="Depression Coaching"),
    ]
    return coaches

def create_clients():
    clients = [
        Client(name="Alice Smith", goals="Overcome anxiety"),
        Client(name="Bob Johnson", goals="Move on from the death of a loved one"),
        Client(name="Charlie Brown", goals="Get over ex-girlfriend"),
        Client(name="David Wilson", goals="Set boundaries with family and friends"),
        Client(name="Eva Green", goals="More confidence"),
    ]
    return clients

def create_sessions(coaches, clients):
    sessions = []
    sessions.append(Session(date=datetime(2024, 7, 25, 9, 0), client_id=clients[0].id, coach_id=coaches[0].id, notes="got better at boundaries", goal_progress=8))
    sessions.append(Session(date=datetime(2024, 7, 25, 10, 0), client_id=clients[1].id, coach_id=coaches[1].id, notes="got back with abusive ex", goal_progress=6))
    sessions.append(Session(date=datetime(2024, 7, 25, 1, 0), client_id=clients[2].id, coach_id=coaches[2].id, notes="got stronger socially", goal_progress=4))
    sessions.append(Session(date=datetime(2024, 7, 25, 2, 0), client_id=clients[3].id, coach_id=coaches[3].id, notes="started boundary work", goal_progress=7))
    sessions.append(Session(date=datetime(2024, 7, 25, 3, 0), client_id=clients[4].id, coach_id=coaches[4].id, notes="learned how to regulate anger", goal_progress=9))
    return sessions

if __name__ == '__main__':
    db_path = os.path.join(os.path.dirname(__file__), 'app.db')

    if os.path.exists(db_path):
        os.remove(db_path)

    with app.app_context():
        print('Creating a new database...')
        db.create_all()

        print("Seeding activities...")
        coaches = create_coaches()
        db.session.add_all(coaches)
        db.session.commit()

        print("Seeding clients...")
        clients = create_clients()
        db.session.add_all(clients)
        db.session.commit()

        print("Seeding sessions...")
        # Reload the activities and clients from the database to ensure ID's are correct
        coaches = Coach.query.all()
        clients = Client.query.all()
        sessions = create_sessions(coaches, clients)
        db.session.add_all(sessions)
        db.session.commit()

        print("Done seeding!")