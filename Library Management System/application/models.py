from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from datetime import datetime, timedelta
import pytz

# create SQLAlchemy instance
db = SQLAlchemy()

IST = pytz.timezone('Asia/Kolkata')

def default_return_date(issue_date):
    return issue_date + timedelta(days=7)

class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column('user_id',db.Integer(),db.ForeignKey('user.id'))
    role_id = db.Column('role_id',db.Integer(),db.ForeignKey('role.id'))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    full_name = db.Column(db.String, unique=False, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String, unique=True, nullable=False)
    last_activity = db.Column(db.DateTime, default=datetime.now(IST))
    ebook_issuee = db.relationship('IssueReturn', backref='user_issued_to', cascade='all, delete-orphan')
    ratings = db.relationship('Ratings', backref='user', cascade='all, delete-orphan')
    roles = db.relationship('Role', secondary='roles_users', backref=db.backref('users',lazy='dynamic'))

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True) # two roles - librarian and user
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.Text)

class Section(db.Model):
    __tablename__ = 'section'
    id = db.Column(db.Integer, primary_key=True)
    section_name = db.Column(db.String, unique=True, nullable=False)
    section_icon = db.Column(db.String, nullable=True)
    description = db.Column(db.Text)
    ebooks = db.relationship('EBook', backref='section', cascade='all, delete-orphan')
    # audit fields ----------------------------------------------
    created_by = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now(IST))
    updated_by = db.Column(db.String, nullable=True)
    updated_date = db.Column(db.DateTime, default=datetime.now(IST), onupdate=datetime.now(IST))

class EBook(db.Model):
    __tablename__ = 'ebook'
    id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'), nullable=False)
    book_name = db.Column(db.String(100), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable= False)
    is_accessible = db.Column(db.Boolean(), default=True)
    # audit fields ----------------------------------------------
    created_by = db.Column(db.String(100), nullable=False) # change to False later
    date_created = db.Column(db.DateTime, default=datetime.now(IST))
    updated_by = db.Column(db.String(100), nullable=True)
    updated_date = db.Column(db.DateTime, default=datetime.now(IST), onupdate=datetime.now(IST))
    ebook = db.relationship('IssueReturn', backref='book_issued', cascade='all, delete-orphan')
    ratings = db.relationship('Ratings', backref='book', cascade='all, delete-orphan')
    
class IssueReturn(db.Model):
    __tablename__ = 'issue_return'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ebook_id = db.Column(db.Integer, db.ForeignKey('ebook.id'), nullable=False)
    issue_date = db.Column(db.DateTime,nullable=True)
    return_date = db.Column(db.DateTime, nullable=True)
    returned_on = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String, nullable=False, default='requested')  # 'granted' or 'revoked'
    # audit fields-------------------------------
    created_by = db.Column(db.String(100), nullable=False) # change to False later
    date_created = db.Column(db.DateTime, default=datetime.now(IST))
    updated_by = db.Column(db.String(100), nullable=True)
    updated_date = db.Column(db.DateTime, default=datetime.now(IST), onupdate=datetime.now(IST))
    
class Ratings(db.Model):
    __tablename__ = 'ratings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ebook_id = db.Column(db.Integer, db.ForeignKey('ebook.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    # audit fields-------------------------------
    created_by = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now(IST))
    updated_by = db.Column(db.String(100), nullable=True)
    updated_date = db.Column(db.DateTime, default=datetime.now(IST), onupdate=datetime.now(IST))