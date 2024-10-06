import os
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from dotenv import load_dotenv
import boto3
import json

# Load environment variables from .env file
load_dotenv()

def get_secret():
    secret_name = os.getenv('SECRET_NAME')  # Fetch from .env file
    region_name = os.getenv('REGION_NAME')  # Fetch from .env file

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = get_secret_value_response['SecretString']
        secret_dict = json.loads(secret)
    except Exception as e:
        raise e

    return secret_dict

# Fetch secrets from AWS Secrets Manager
secrets = get_secret()

# Instantiate app, set attributes
app = Flask(__name__)

# Configure the app using the secrets fetched from AWS Secrets Manager
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{secrets['username']}:{secrets['password']}@{secrets['host']}:{secrets['port']}/{secrets['dbname']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_fallback_secret_key')
app.json.compact = False

# Define metadata, instantiate db
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)
migrate = Migrate(app, db)
db.init_app(app)

# Instantiate REST API
api = Api(app)

# Instantiate CORS
CORS(app)