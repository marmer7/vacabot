from datetime import datetime

from app import db


class Itinerary(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    destination = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    is_budget_friendly = db.Column(db.BOOLEAN, nullable=True)
    interests = db.Column(db.ARRAY(db.Text), nullable=True)
    markdown = db.Column(db.Text, nullable=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
    modified_date = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True
    )
    job_id = db.Column(db.String(64), nullable=True)
