# backend/models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

class Scan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scan_id = db.Column(db.String, unique=True, nullable=False)
    network = db.Column(db.String)
    status = db.Column(db.String, default='started')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    result_path = db.Column(db.String)
