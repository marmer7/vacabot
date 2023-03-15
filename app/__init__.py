import os

import openai
from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from redis import Redis
from rq import Queue

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


# Connect to Redis and create a task queue
redis_conn = Redis.from_url(os.environ.get("REDIS_URL"))
task_queue = Queue(connection=redis_conn)


# Import the routes and models modules
from app import models, routes  # noqa
