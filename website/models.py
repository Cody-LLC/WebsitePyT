from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    time = db.Column(db.String(50), nullable=False)
    day = db.Column(db.String(20))  # Store the day of the appointment (e.g., Monday, Tuesday)
    is_admin = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(150), unique=True)  # Add the email field

    def __repr__(self):
        return f'<User {self.name}, Time: {self.time}, Day: {self.day}>'
