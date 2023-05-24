from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid 
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow 
import secrets

# set variables for class instantiation
login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(150), nullable=True, default='')
    last_name = db.Column(db.String(150), nullable=True, default='')
    email = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String, nullable=True, default='')
    token = db.Column(db.String, default='', unique=True )
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, email, first_name='', last_name='', password=''):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'User {self.email}'
    

class Book(db.Model):
    contributor_token = db.Column(db.String) #----------- token of the user who contributed the book
    local_id = db.Column(db.String, primary_key=True) #-- locally-stored id for the book
    isbn = db.Column(db.Integer, default=1001101000001) # isbn for this book (format: xxx-x-xx-xxxxxx-x)
    title = db.Column(db.String(150), default='')
    author = db.Column(db.String(150), default='')
    page_count = db.Column(db.Integer, default=0)
    is_hardcover = db.Column(db.Boolean, default=False)

    def __init__(self, contributor_token, isbn, title='', author='', page_count=0, is_hardcover=False):
        self.contributor_token = contributor_token
        self.local_id = self.set_id()
        self.isbn = isbn
        self.title = title
        self.author = author
        self.page_count = page_count

    def set_id(self):
        return secrets.token_urlsafe()
    
    def __repr__(self):
        return f'"{self.title}" by {self.author}'
    
class BookSchema(ma.Schema):
    class Meta:
        fields = ['contributor_token', 'local_id', 'isbn', 'title', 'author', 'page_count']

book_schema = BookSchema()
books_schema = BookSchema(many=True)