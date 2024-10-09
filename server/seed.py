from config import app, db
from models import Coach, Client, Session, CoachClient
import os
from datetime import datetime
from werkzeug.security import generate_password_hash

def create_coaches():
    coaches = [
        Coach(name="Matilda Hubert", specialization="Trauma Coaching", username="matilda", password_hash=generate_password_hash("password123")),
        Coach(name="Ricky Milton", specialization="Mindfulness and Performance Coaching", username="ricky", password_hash=generate_password_hash("password123")),
        Coach(name="Sam Morton", specialization="Depression Coaching", username="sam", password_hash=generate_password_hash("password123")),
        Coach(name="Denise Lawson", specialization="Trauma Coaching", username="denise", password_hash=generate_password_hash("password123")),
        Coach(name="Natalie Ventura", specialization="Mindfulness and Performance Coaching", username="natalie", password_hash=generate_password_hash("password123")),
        Coach(name="Veronica Bolton", specialization="Depression Coaching", username="veronica", password_hash=generate_password_hash("password123")),
    ]
    return coaches

def create_clients():
    clients = [
        Client(name="Alice Smith", goals="Overcome anxiety"),
        Client(name="Bob Johnson", goals="Move on from the death of a loved one"),
        Client(name="Charlie Brown", goals="Get over ex-girlfriend"),
        Client(name="David Wilson", goals="Set boundaries with family and friends"),
        Client(name="Eva Green", goals="More confidence"),
        Client(name="Hannah White", goals="Cope with social anxiety"),
        Client(name="Sophia Davis", goals="Recover from a traumatic event"),
        Client(name="Lily Thompson", goals="Manage chronic stress"),
        Client(name="Jack Lewis", goals="Enhance focus during work"),
        Client(name="Amelia Baker", goals="Overcome fear of public speaking"),
        Client(name="Michael Harris", goals="Develop mindfulness habits"),
        Client(name="Daniel King", goals="Work through childhood trauma"),
        Client(name="Ella Wright", goals="Heal from abusive relationship"),
        Client(name="Zoe Scott", goals="Manage anxiety from past experiences"),
        Client(name="Logan Adams", goals="Improve stress management"),
        Client(name="Abigail Martinez", goals="Increase mindfulness in daily activities"),
        Client(name="Owen Mitchell", goals="Balance work and personal life"),
        Client(name="Mason Carter", goals="Reduce depressive symptoms"),
        Client(name="Mia Thompson", goals="Enhance mental well-being"),
        Client(name="Liam Anderson", goals="Develop positive coping strategies"),
    ]
    return clients

def create_sessions(coaches, clients):
    base_sessions = [
        Session(date=datetime(2024, 10, 25, 9, 0), client_id=clients[0].id, coach_id=coaches[0].id, notes="Got better at boundaries", goal_progress=8),
        Session(date=datetime(2024, 10, 25, 10, 0), client_id=clients[1].id, coach_id=coaches[1].id, notes="Got back with abusive ex", goal_progress=6),
        Session(date=datetime(2024, 10, 25, 1, 0), client_id=clients[2].id, coach_id=coaches[2].id, notes="Got stronger socially", goal_progress=4),
        Session(date=datetime(2024, 10, 19, 9, 0), client_id=clients[3].id, coach_id=coaches[0].id, notes="Working on setting boundaries", goal_progress=7),
        Session(date=datetime(2024, 10, 19, 10, 0), client_id=clients[4].id, coach_id=coaches[0].id, notes="Building confidence", goal_progress=9),
        Session(date=datetime(2024, 10, 20, 11, 0), client_id=clients[5].id, coach_id=coaches[1].id, notes="Coping with social anxiety", goal_progress=6),
        Session(date=datetime(2024, 10, 20, 9, 0), client_id=clients[6].id, coach_id=coaches[1].id, notes="Recovering from trauma", goal_progress=8),
        Session(date=datetime(2024, 10, 21, 10, 0), client_id=clients[7].id, coach_id=coaches[2].id, notes="Managing chronic stress", goal_progress=7),
        Session(date=datetime(2024, 10, 21, 11, 0), client_id=clients[8].id, coach_id=coaches[2].id, notes="Enhancing focus", goal_progress=8),
        Session(date=datetime(2024, 10, 22, 9, 0), client_id=clients[9].id, coach_id=coaches[3].id, notes="Overcoming fear of public speaking", goal_progress=6),
        Session(date=datetime(2024, 10, 22, 10, 0), client_id=clients[10].id, coach_id=coaches[3].id, notes="Developing mindfulness habits", goal_progress=9),
        Session(date=datetime(2024, 10, 23, 11, 0), client_id=clients[11].id, coach_id=coaches[4].id, notes="Working through childhood trauma", goal_progress=8),
        Session(date=datetime(2024, 10, 23, 9, 0), client_id=clients[12].id, coach_id=coaches[4].id, notes="Healing from abusive relationship", goal_progress=7),
        Session(date=datetime(2024, 10, 24, 10, 0), client_id=clients[13].id, coach_id=coaches[5].id, notes="Managing anxiety from past experiences", goal_progress=6),
        Session(date=datetime(2024, 10, 24, 11, 0), client_id=clients[14].id, coach_id=coaches[5].id, notes="Improving stress management", goal_progress=9),
    ]   

    # adding more sessions for each coach anf spreading thenm out
    additional_sessions = []
    for i, coach in enumerate(coaches):
        for j in range(10):
            # Spread out sessions in October, adjusting the dates and times
            day_offset = j // 2 + 1  # Spreading sessions across different days
            hour_offset = 9 + (j % 3)  # Changing the hours for variety
            additional_sessions.append(
                Session(
                    date=datetime(2024, 10, day_offset + i, hour_offset, 0),  # Adjusted to October
                    client_id=clients[(i + j) % len(clients)].id,  # Rotating through clients
                    coach_id=coach.id,
                    notes=f"Session with {clients[(i + j) % len(clients)].name}",
                    goal_progress=(j % 10) + 1
                )
            )

    return base_sessions + additional_sessions

def create_coach_clients(coaches, clients):
    coach_clients = [
        CoachClient(coach_id=coaches[0].id, client_id=clients[0].id, notes="Initial consultation"),
        CoachClient(coach_id=coaches[1].id, client_id=clients[1].id, notes="Ongoing therapy"),
        CoachClient(coach_id=coaches[2].id, client_id=clients[2].id, notes="Review session"),
    ]
    return coach_clients
if __name__ == '__main__':
    with app.app_context():
        print('Creating a new database...')
        db.create_all()

        print("Seeding activities...")
        coaches = create_coaches()
        db.session.add_all(coaches)
        db.session.commit()

        clients = create_clients()
        db.session.add_all(clients)
        db.session.commit()

        sessions = create_sessions(coaches, clients)
        db.session.add_all(sessions)
        db.session.commit()

        coach_clients = create_coach_clients(coaches, clients)
        db.session.add_all(coach_clients)
        db.session.commit()

        print("Done seeding!")