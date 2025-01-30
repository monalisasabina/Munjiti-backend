from flask_sqlalchemy import SQLAlchemy

from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

db = SQLAlchemy()

class User (db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    role=db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(100))
    password =  db.Column(db.String(100))


class Project(db.Model, SerializerMixin):
     __tablename__ = 'projects'

     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(100), nullable=False)
     description = db.Column(db.String, nullable=False)
     date_added = db.Column(db.DateTime, default=datetime.utcnow)


class Notice(db.Model, SerializerMixin):
    __tablename__='notices'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)


class Downloads(db.Model, SerializerMixin):
    __tablename__ = 'downloads'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String, nullable=False)
    file_url = db. Column(db.String(300), nullable=False) #url/ path of the file
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

class ContactMessage(db.Model,SerializerMixin):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    sender_firstname = db.Column(db.String(50), nullable=False)
    sender_lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String, nullable=False)
    message = db.Column(db.String, nullable=False)

class Notification(db.Model, SerializerMixin):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255), nullable=True)
    is_read = db.Column(db.Boolean, default=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)