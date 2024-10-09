import os
from dotenv import load_dotenv
import boto3
import json
from flask import Flask
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
        print(f"Error fetching secret: {e}")
        raise e

    # Check for required keys
    required_keys = ['username', 'password', 'host', 'port', 'dbname', 'secret_key']
    for key in required_keys:
        if key not in secret_dict:
            raise KeyError(f"Missing required key in secrets: {key}")

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
    if os.getenv('FLASK_ENV') == 'production':
        SQLALCHEMY_DATABASE_URI = f"postgresql://{secrets['username']}:{secrets['password']}@{secrets['host']}:{secrets['port']}/{secrets['dbname']}"
    else:
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'instance', 'app.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = secrets.get('secret_key')

# Migrate configuration
migrate = Migrate()

# Create and configure Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Register the app with db and migrate
db.init_app(app)
migrate.init_app(app, db)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)