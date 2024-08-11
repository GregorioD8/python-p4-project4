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
        # Original Clients
        Client(name="Alice Smith", goals="Overcome anxiety"),
        Client(name="Bob Johnson", goals="Move on from the death of a loved one"),
        Client(name="Charlie Brown", goals="Get over ex-girlfriend"),
        Client(name="David Wilson", goals="Set boundaries with family and friends"),
        Client(name="Eva Green", goals="More confidence"),
        
        # New Clients for Matilda Hubert
        Client(name="Hannah White", goals="Cope with social anxiety"),
        Client(name="Sophia Davis", goals="Recover from a traumatic event"),
        Client(name="Lily Thompson", goals="Manage chronic stress"),

        # New Clients for Ricky Milton
        Client(name="Jack Lewis", goals="Enhance focus during work"),
        Client(name="Amelia Baker", goals="Overcome fear of public speaking"),
        Client(name="Michael Harris", goals="Develop mindfulness habits"),

        # New Clients for Sam Morton
        Client(name="Emily Wilson", goals="Reduce symptoms of depression"),
        Client(name="Lucas Clark", goals="Improve self-esteem"),
        Client(name="Grace Walker", goals="Manage sadness and loneliness"),

        # New Clients for Denise Lawson
        Client(name="Daniel King", goals="Work through childhood trauma"),
        Client(name="Ella Wright", goals="Heal from abusive relationship"),
        Client(name="Zoe Scott", goals="Manage anxiety from past experiences"),

        # New Clients for Natalie Ventura
        Client(name="Logan Adams", goals="Improve stress management"),
        Client(name="Abigail Martinez", goals="Increase mindfulness in daily activities"),
        Client(name="Owen Mitchell", goals="Balance work and personal life"),

        # New Clients for Veronica Bolton
        Client(name="Mason Carter", goals="Reduce depressive symptoms"),
        Client(name="Mia Thompson", goals="Enhance mental well-being"),
        Client(name="Liam Anderson", goals="Develop positive coping strategies"),
    ]
    return clients

def create_sessions(coaches, clients):
    sessions = []
    
    # Original Sessions
    sessions.append(Session(date=datetime(2024, 7, 25, 9, 0), client_id=clients[0].id, coach_id=coaches[0].id, notes="Got better at boundaries", goal_progress=8))
    sessions.append(Session(date=datetime(2024, 7, 25, 10, 0), client_id=clients[1].id, coach_id=coaches[1].id, notes="Got back with abusive ex", goal_progress=6))
    sessions.append(Session(date=datetime(2024, 7, 25, 1, 0), client_id=clients[2].id, coach_id=coaches[2].id, notes="Got stronger socially", goal_progress=4))
    sessions.append(Session(date=datetime(2024, 7, 25, 2, 0), client_id=clients[3].id, coach_id=coaches[3].id, notes="Started boundary work", goal_progress=7))
    sessions.append(Session(date=datetime(2024, 7, 25, 3, 0), client_id=clients[4].id, coach_id=coaches[4].id, notes="Learned how to regulate anger", goal_progress=9))
    
    # New Sessions for Matilda Hubert
    sessions.append(Session(date=datetime(2024, 8, 1, 9, 0), client_id=clients[5].id, coach_id=coaches[0].id, notes="Worked on social anxiety coping strategies", goal_progress=7))
    sessions.append(Session(date=datetime(2024, 8, 1, 10, 0), client_id=clients[6].id, coach_id=coaches[0].id, notes="Discussed trauma recovery methods", goal_progress=8))
    sessions.append(Session(date=datetime(2024, 8, 1, 11, 0), client_id=clients[7].id, coach_id=coaches[0].id, notes="Managed chronic stress with techniques", goal_progress=6))

    # New Sessions for Ricky Milton
    sessions.append(Session(date=datetime(2024, 8, 2, 9, 0), client_id=clients[8].id, coach_id=coaches[1].id, notes="Enhanced focus using mindfulness", goal_progress=8))
    sessions.append(Session(date=datetime(2024, 8, 2, 10, 0), client_id=clients[9].id, coach_id=coaches[1].id, notes="Overcame public speaking fear", goal_progress=7))
    sessions.append(Session(date=datetime(2024, 8, 2, 11, 0), client_id=clients[10].id, coach_id=coaches[1].id, notes="Established daily mindfulness habits", goal_progress=9))

    # New Sessions for Sam Morton
    sessions.append(Session(date=datetime(2024, 8, 3, 9, 0), client_id=clients[11].id, coach_id=coaches[2].id, notes="Reduced depressive symptoms", goal_progress=6))
    sessions.append(Session(date=datetime(2024, 8, 3, 10, 0), client_id=clients[12].id, coach_id=coaches[2].id, notes="Improved self-esteem and confidence", goal_progress=8))
    sessions.append(Session(date=datetime(2024, 8, 3, 11, 0), client_id=clients[13].id, coach_id=coaches[2].id, notes="Managed sadness and loneliness", goal_progress=7))

    # New Sessions for Denise Lawson
    sessions.append(Session(date=datetime(2024, 8, 4, 9, 0), client_id=clients[14].id, coach_id=coaches[3].id, notes="Explored childhood trauma", goal_progress=8))
    sessions.append(Session(date=datetime(2024, 8, 4, 10, 0), client_id=clients[15].id, coach_id=coaches[3].id, notes="Healed from abusive relationship", goal_progress=7))
    sessions.append(Session(date=datetime(2024, 8, 4, 11, 0), client_id=clients[16].id, coach_id=coaches[3].id, notes="Managed anxiety from past experiences", goal_progress=6))

    # New Sessions for Natalie Ventura
    sessions.append(Session(date=datetime(2024, 8, 5, 9, 0), client_id=clients[17].id, coach_id=coaches[4].id, notes="Improved stress management techniques", goal_progress=9))
    sessions.append(Session(date=datetime(2024, 8, 5, 10, 0), client_id=clients[18].id, coach_id=coaches[4].id, notes="Increased mindfulness in daily life", goal_progress=8))
    sessions.append(Session(date=datetime(2024, 8, 5, 11, 0), client_id=clients[19].id, coach_id=coaches[4].id, notes="Balanced work and personal life", goal_progress=7))

    # New Sessions for Veronica Bolton
    sessions.append(Session(date=datetime(2024, 8, 6, 9, 0), client_id=clients[20].id, coach_id=coaches[5].id, notes="Reduced depressive symptoms", goal_progress=8))
    sessions.append(Session(date=datetime(2024, 8, 6, 10, 0), client_id=clients[21].id, coach_id=coaches[5].id, notes="Enhanced mental well-being", goal_progress=7))
    sessions.append(Session(date=datetime(2024, 8, 6, 11, 0), client_id=clients[22].id, coach_id=coaches[5].id, notes="Developed positive coping strategies", goal_progress=8))

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