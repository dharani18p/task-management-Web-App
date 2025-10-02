from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    tasks = db.relationship('Task', backref='assigned_user', lazy=True)

class Task(db.Model):
    __tablename__ = "tasks"
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    assigned_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    priority = db.Column(db.String(20), nullable=True)
    status = db.Column(db.String(50), default='pending')
    due_date = db.Column(db.Date, nullable=True)
    due_time = db.Column(db.Time, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
