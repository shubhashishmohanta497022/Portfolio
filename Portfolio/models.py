from datetime import datetime
from extensions import db  # Import db instance from extensions.py
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# ... existing code for User, Project, Skill, etc. ...
class User(UserMixin, db.Model):
    """Admin User Model"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Project(db.Model):
    """Portfolio Project Model"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    github_link = db.Column(db.String(200), nullable=True)
    live_link = db.Column(db.String(200), nullable=True)
    image_url = db.Column(db.String(200), nullable=True, default='https://placehold.co/600x400/2d3748/ffffff?text=Project')
    tags = db.Column(db.String(200), nullable=True) # Comma-separated tags
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Project {self.title}>'

class Skill(db.Model):
    """Skills Model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    level = db.Column(db.Integer, nullable=False, default=80) # Percentage
    category = db.Column(db.String(80), nullable=True, default='Programming Language')

    def __repr__(self):
        return f'<Skill {self.name}>'

class Certification(db.Model):
    """Certifications Model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    issuer = db.Column(db.String(120), nullable=False)
    date_issued = db.Column(db.Date, nullable=False)
    credential_link = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f'<Certification {self.name}>'

class Message(db.Model):
    """Contact Form Messages Model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Message from {self.name}>'

class BlogPost(db.Model):
    """Blog Post Model"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False, default='Admin')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    slug = db.Column(db.String(200), unique=True, nullable=False)

    def __repr__(self):
        return f'<BlogPost {self.title}>'

class Visit(db.Model):
    """Visit Tracker Model"""
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(45)) # Supports IPv4 and IPv6
    user_agent = db.Column(db.String(255), nullable=True) # <-- ADD THIS LINE
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Visit from {self.ip_address} on {self.timestamp}>'

