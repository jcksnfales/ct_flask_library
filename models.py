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
    

# class Car(db.Model):
#     user_token = db.Column(db.String)
#     id = db.Column(db.String, primary_key = True)
#     nickname = db.Column(db.String(150), default = '')
#     make = db.Column(db.String(150), default = '')
#     model = db.Column(db.String(150), default = '')
#     prodyear = db.Column(db.Integer)
#     mileage = db.Column(db.Integer, default = 0)

#     def __init__(self, user_token, nickname='', make='', model='', prodyear='', mileage=0):
#         self.user_token = user_token
#         self.id = self.set_id()
#         self.nickname = nickname 
#         self.make = make
#         self.model = model 
#         self.prodyear = prodyear
#         self.mileage = mileage

#     def set_id(self):
#         return secrets.token_urlsafe()
    
#     def __repr__(self):
#         # using a list comprehension, get a combined string of the non-null values for prodyear, make, and model
#         car_identity = ' '.join([str(field) for field in [self.prodyear, self.make, self.model] if field])
#         # if this car has no nickname, just return car_identity;
#         # otherwise, return the nickname in quotes followed by car_identity
#         return car_identity if not self.nickname else f'"{self.nickname}", {car_identity}'
    
# class CarSchema(ma.Schema):
#     class Meta:
#         fields = ['user_token', 'id', 'nickname', 'make', 'model', 'prodyear', 'mileage']

# car_schema = CarSchema()
# cars_schema = CarSchema(many=True)