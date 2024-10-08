import os
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from dotenv import load_dotenv
from app import Clients, ClientsById, Coaches, Sessions, SessionsById, CoachClientResource
import boto3
import json

#load environment variables from .env file
load_dotenv()

# fetch secrets from AWS Secrets Manager
def get_secret():
    secret_name = os.getenv('SECRET_NAME')  # Get secret name from .env
    region_name = os.getenv('AWS_REGION')   # Get region name from .env

    # Create an Secrets Manager client
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

# Instantiate Flask app
app = Flask(__name__)

# Configure the app using the secrets fetched from AWS Secrets Manager
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{secrets['username']}:{secrets['password']}@{secrets['host']}:{secrets['port']}/{secrets['dbname']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Fetch and configure secret key from Secrets Manager
app.config['SECRET_KEY'] = secrets.get('secret_key')

# Enable JSON pretty print
app.json.compact = False

# Define metadata, instantiate db
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

# Initialize SQLAlchemy and Migrate
db = SQLAlchemy(metadata=metadata)
db.init_app(app)
migrate = Migrate(app, db)

# Import models to ensure they are registered with SQLAlchemy
from models import Coach, Client, Session, CoachClient

# Instantiate REST API
api = Api(app)

# Enable CORS
CORS(app)

# Define your resources and add them to the API
api.add_resource(Clients, '/clients')
api.add_resource(ClientsById, '/clients/<int:id>')
api.add_resource(Coaches, '/coaches')
api.add_resource(Sessions, '/sessions')
api.add_resource(SessionsById, '/sessions/<int:session_id>')
api.add_resource(CoachClientResource, '/coach_clients')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')