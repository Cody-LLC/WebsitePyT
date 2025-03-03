from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer), primary_key=True)
    data = db.Column(db.string(100))
    date = db.column(db.DateTime(timezone=True), default=func.now())
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.column(db.String(150))
    time = db.Column(db.String(150))