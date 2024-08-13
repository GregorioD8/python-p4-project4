from app import app
from models import db, Coach, Client, Session, CoachClient
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
        # New clients
        Client(name="Hannah White", goals="Cope with social anxiety"),
        Client(name="Sophia Davis", goals="Recover from a traumatic event"),
        Client(name="Lily Thompson", goals="Manage chronic stress"),
        Client(name="Jack Lewis", goals="Enhance focus during work"),
        Client(name="Amelia Baker", goals="Overcome fear of public speaking"),
        Client(name="Michael Harris", goals="Develop mindfulness habits"),
        # Clients for Denise Lawson, Natalie Ventura, and Veronica Bolton
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
    sessions = [
        Session(date=datetime(2024, 7, 25, 9, 0), client_id=clients[0].id, coach_id=coaches[0].id, notes="Got better at boundaries", goal_progress=8),
        Session(date=datetime(2024, 7, 25, 10, 0), client_id=clients[1].id, coach_id=coaches[1].id, notes="Got back with abusive ex", goal_progress=6),
        Session(date=datetime(2024, 7, 25, 1, 0), client_id=clients[2].id, coach_id=coaches[2].id, notes="Got stronger socially", goal_progress=4),
        # New sessions
        Session(date=datetime(2024, 8, 1, 9, 0), client_id=clients[5].id, coach_id=coaches[0].id, notes="Worked on social anxiety coping strategies", goal_progress=7),
        Session(date=datetime(2024, 8, 1, 10, 0), client_id=clients[6].id, coach_id=coaches[0].id, notes="Discussed trauma recovery methods", goal_progress=8),
        Session(date=datetime(2024, 8, 1, 11, 0), client_id=clients[7].id, coach_id=coaches[0].id, notes="Managed chronic stress with techniques", goal_progress=6),
        Session(date=datetime(2024, 8, 2, 9, 0), client_id=clients[8].id, coach_id=coaches[1].id, notes="Enhanced focus using mindfulness", goal_progress=8),
        Session(date=datetime(2024, 8, 2, 10, 0), client_id=clients[9].id, coach_id=coaches[1].id, notes="Overcame public speaking fear", goal_progress=7),
        Session(date=datetime(2024, 8, 2, 11, 0), client_id=clients[10].id, coach_id=coaches[1].id, notes="Established daily mindfulness habits", goal_progress=9),
        # Clients with consecutive sessions with different coaches
        Session(date=datetime(2024, 8, 3, 9, 0), client_id=clients[5].id, coach_id=coaches[1].id, notes="Follow-up session on anxiety", goal_progress=8),
        Session(date=datetime(2024, 8, 4, 9, 0), client_id=clients[6].id, coach_id=coaches[2].id, notes="Discussing trauma with a new approach", goal_progress=7),
        # Sessions for Denise Lawson
        Session(date=datetime(2024, 8, 5, 9, 0), client_id=clients[11].id, coach_id=coaches[3].id, notes="Explored childhood trauma", goal_progress=8),
        Session(date=datetime(2024, 8, 5, 10, 0), client_id=clients[12].id, coach_id=coaches[3].id, notes="Healed from abusive relationship", goal_progress=7),
        Session(date=datetime(2024, 8, 5, 11, 0), client_id=clients[13].id, coach_id=coaches[3].id, notes="Managed anxiety from past experiences", goal_progress=6),
        # Sessions for Natalie Ventura
        Session(date=datetime(2024, 8, 6, 9, 0), client_id=clients[14].id, coach_id=coaches[4].id, notes="Improved stress management techniques", goal_progress=9),
        Session(date=datetime(2024, 8, 6, 10, 0), client_id=clients[15].id, coach_id=coaches[4].id, notes="Increased mindfulness in daily life", goal_progress=8),
        Session(date=datetime(2024, 8, 6, 11, 0), client_id=clients[16].id, coach_id=coaches[4].id, notes="Balanced work and personal life", goal_progress=7),
        # Sessions for Veronica Bolton
        Session(date=datetime(2024, 8, 7, 9, 0), client_id=clients[17].id, coach_id=coaches[5].id, notes="Reduced depressive symptoms", goal_progress=8),
        Session(date=datetime(2024, 8, 7, 10, 0), client_id=clients[18].id, coach_id=coaches[5].id, notes="Enhanced mental well-being", goal_progress=7),
        Session(date=datetime(2024, 8, 7, 11, 0), client_id=clients[19].id, coach_id=coaches[5].id, notes="Developed positive coping strategies", goal_progress=8),
    ]
    return sessions

def create_coach_clients(coaches, clients):
    coach_clients = [
        CoachClient(coach_id=coaches[0].id, client_id=clients[0].id, notes="Initial consultation"),
        CoachClient(coach_id=coaches[1].id, client_id=clients[1].id, notes="Ongoing therapy"),
        CoachClient(coach_id=coaches[2].id, client_id=clients[2].id, notes="Review session"),
        # New Coach-Client relationships
        CoachClient(coach_id=coaches[0].id, client_id=clients[5].id, notes="Working on social anxiety"),
        CoachClient(coach_id=coaches[0].id, client_id=clients[6].id, notes="Recovering from trauma"),
        CoachClient(coach_id=coaches[0].id, client_id=clients[7].id, notes="Managing stress"),
        CoachClient(coach_id=coaches[1].id, client_id=clients[8].id, notes="Enhancing focus"),
        CoachClient(coach_id=coaches[1].id, client_id=clients[9].id, notes="Overcoming fear of public speaking"),
        CoachClient(coach_id=coaches[1].id, client_id=clients[10].id, notes="Developing mindfulness habits"),
        # Clients meeting with two coaches
        CoachClient(coach_id=coaches[1].id, client_id=clients[5].id, notes="Follow-up after working on social anxiety"),
        CoachClient(coach_id=coaches[2].id, client_id=clients[6].id, notes="Exploring trauma with new methods"),
        # Relationships for Denise Lawson
        CoachClient(coach_id=coaches[3].id, client_id=clients[11].id, notes="Childhood trauma exploration"),
        CoachClient(coach_id=coaches[3].id, client_id=clients[12].id, notes="Healing from abusive relationship"),
        CoachClient(coach_id=coaches[3].id, client_id=clients[13].id, notes="Managing anxiety"),
        # Relationships for Natalie Ventura
        CoachClient(coach_id=coaches[4].id, client_id=clients[14].id, notes="Stress management"),
        CoachClient(coach_id=coaches[4].id, client_id=clients[15].id, notes="Mindfulness enhancement"),
        CoachClient(coach_id=coaches[4].id, client_id=clients[16].id, notes="Work-life balance"),
        # Relationships for Veronica Bolton
        CoachClient(coach_id=coaches[5].id, client_id=clients[17].id, notes="Depression reduction"),
        CoachClient(coach_id=coaches[5].id, client_id=clients[18].id, notes="Mental well-being improvement"),
        CoachClient(coach_id=coaches[5].id, client_id=clients[19].id, notes="Positive coping strategies development"),
    ]
    return coach_clients

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
        sessions = create_sessions(coaches, clients)
        db.session.add_all(sessions)
        db.session.commit()

        print("Seeding coach-client relationships...")
        coach_clients = create_coach_clients(coaches, clients)
        db.session.add_all(coach_clients)
        db.session.commit()

        print("Done seeding!")