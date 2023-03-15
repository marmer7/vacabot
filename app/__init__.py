import os

import openai
from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import config

# Load environment variables from .env
load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")


# Create the Flask app and configure the database connection
app = Flask(__name__)
app.config.from_object(config[os.environ.get("ENVIRONMENT", "development")])


# Create the database object and the migration object
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Import the routes and models modules
from app import models, routes  # noqa
