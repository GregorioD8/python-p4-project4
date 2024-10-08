import os
from dotenv import load_dotenv
import boto3
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_migrate import Migrate

# Load environment variables from .env file
load_dotenv()

# Fetch secrets from AWS Secrets Manager
def get_secret():
    secret_name = os.getenv('SECRET_NAME')  # Get secret name from .env
    region_name = os.getenv('AWS_REGION')   # Get region name from .env

    # Create a Secrets Manager client
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

# Database configuration
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

# Initialize SQLAlchemy
db = SQLAlchemy(metadata=metadata)

# Flask app configuration using secrets fetched from AWS Secrets Manager
class Config:
    SQLALCHEMY_DATABASE_URI = f"postgresql://{secrets['username']}:{secrets['password']}@{secrets['host']}:{secrets['port']}/{secrets['dbname']}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = secrets.get('secret_key')

# Migrate configuration
migrate = Migrate()