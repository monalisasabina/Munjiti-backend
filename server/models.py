from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates, joinedload
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from flask_bcrypt import Bcrypt

# for encrypting data
from cryptography.fernet import Fernet
import os

# Load or generate a secret key (use environment variable in production)
SECRET_KEY = os.getenv("SECRET_KEY", Fernet.generate_key().decode())  
cipher = Fernet(SECRET_KEY.encode())

db = SQLAlchemy()
bcrypt = Bcrypt()

class User (db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    role=db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(100), nullable= False)
    email = db.Column(db.String, nullable= False)
    _password_hash =  db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

    # validating the email address
    @validates('email')
    def validate_email(self, key, address):
        if '@' not in address:
            raise ValueError('Please include "@"')
        return address

    # password hashing
    @hybrid_property
    def password_hash(self):
        return self._password_hash

    @password_hash.setter
    def password_hash(self, password):

        password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))    
    



class Pastor(db.Model, SerializerMixin):
    __tablename__ = 'pastors'        

    id= db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Pastor: Name: {self.firstname} {self.lastname} | Role: {self.role} | Date added: {self.date_added} >"

    #validations
    @validates('date_added')
    def validate_date_added(self, key, date_added):
        if date_added > datetime.utcnow():
            raise ValueError("date_added cannot be in the future")
        return date_added
    


class Project(db.Model, SerializerMixin):
     __tablename__ = 'projects'

     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(100), nullable=False)
     description = db.Column(db.String, nullable=False)
     date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
     # Relationship
     ministries = db.relationship('Ministry', secondary='ministry_projects', back_populates= 'projects')
     images = db.relationship('ProjectImage', back_populates='project', cascade="all, delete-orphan")

     # Prevent circular reference by excluding 'project' from serialization
     serialize_rules = ('-ministries.project', '-images.project') 

     #validations
     @validates('date_added')
     def validate_date_added(self, key, date_added):
        if date_added > datetime.utcnow():
            raise ValueError("date_added cannot be in the future")
        return date_added 

     def __repr__(self):
         return f"<Project: Name:{self.name} | Date Added: {self.date_added} >"   
     

class ProjectImage(db.Model, SerializerMixin):
    __tablename__='project_images'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete="CASCADE"), nullable=False)
    image_url = db.Column(db.String, nullable=False)

    # Relation with the project
    project = db.relationship('Project', back_populates='images')

    # Prevent circular reference
    serialize_rules = ('-project.images',)



class Ministry(db.Model, SerializerMixin):
    __tablename__ = 'ministries'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    projects = db.relationship('Project', secondary='ministry_projects', back_populates='ministries')
    
    serialize_rules = ('-projects.ministries',)  # Prevent circular references 
    
    def __repr__(self):
        return f"<Ministry {self.name}>"
    


# association table
# table links the ministries and projects in a many to many r/ship
class MinistryProject(db.Model, SerializerMixin):
    __tablename__='ministry_projects'

    serialize_rules = ('-ministry.projects', '-project.ministries') 

    id = db.Column(db.Integer, primary_key=True)

    ministry_id =db.Column(db.Integer, db.ForeignKey('ministries.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))

    # ministry = db.relationship('Ministry', back_populates='projects')
    # project = db.relationship('Project', back_populates='ministries')

    def __repr__(self):
        return f"<MinistryProject Ministry: {self.ministry_id}, Project: {self.project_id}>"



class Notice(db.Model, SerializerMixin):
    __tablename__='notices'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    notice_text = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    #validations
    @validates('date_added')
    def validate_date_added(self, key, date_added):
        if date_added > datetime.utcnow():
            raise ValueError("date_added cannot be in the future")
        return date_added

    def __repr__(self):
        return f"<Notice {self.title}>"



class Downloads(db.Model, SerializerMixin):
    __tablename__ = 'downloads'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String, nullable=False)
    file_url = db. Column(db.String(300), nullable=False) #url/ path of the file
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    #validations
    @validates('date_added')
    def validate_date_added(self, key, date_added):
        if date_added > datetime.utcnow():
            raise ValueError("date_added cannot be in the future")
        return date_added

    def __repr__(self):
        return f"<Download {self.name}>"



class ContactMessage(db.Model,SerializerMixin):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    sender_firstname = db.Column(db.String(50), nullable=False)
    sender_lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String, nullable=False)
    mobile_number = db.Column(db.String) 
    message = db.Column(db.String, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    notifications = db.relationship("Notification", back_populates="contact_message", lazy=True, passive_deletes=True)

    def __repr__(self):
        return f"<Message from {self.sender_firstname} {self.sender_lastname}>"



class Notification(db.Model, SerializerMixin):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255), nullable=True)
    is_read = db.Column(db.Boolean, default=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign Contact_message ID
    contact_message_id = db.Column(db.Integer, db.ForeignKey('messages.id',ondelete='CASCADE'))

    # Relation between contact message and notification
    contact_message = db.relationship('ContactMessage', back_populates='notifications')

    #validations
    @validates('date_added')
    def validate_date_added(self, key, date_added):
        if date_added > datetime.utcnow():
            raise ValueError("date_added cannot be in the future")
        return date_added

    def __repr__(self):
      return f"<Notification {self.message[:20]}...>" 
    

class Gallery(db.Model, SerializerMixin):
    __tablename__='gallery'

    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String, nullable=True)
    description = db.Column(db.String, nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    @validates('image_url')
    def validate_image_url(self, key, value):
        if not value:
            raise ValueError("Image URL cannot be empty")
        return value


    def __repr__(self):
        return f"<Gallery: Pic no:{self.id} | Image: {self.image_url} | Date added: {self.date_added}"
    
