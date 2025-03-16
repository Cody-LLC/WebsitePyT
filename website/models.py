from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    time = db.Column(db.String(150))
    day = db.Column(db.String(20))  # Store the day of the appointment (e.g., Monday, Tuesday)
    week_number = db.Column(db.Integer)  # Store the week number to reset weekly
    is_admin = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<Admin {self.email}>'