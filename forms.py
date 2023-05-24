from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo

class UserLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message='Please enter a valid email address.')])
    password = PasswordField('Password', validators=[DataRequired()])
    submit_button = SubmitField('Submit')

class UserRegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message='Please enter a valid email address.')])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password_confirm', message='Passwords must match.')])
    password_confirm = PasswordField('Confirm Password')
    submit_button = SubmitField('Submit')

class BookContributionForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    isbn = IntegerField('ISBN', validators=[DataRequired()])
    author = StringField('Author Name')
    page_count = IntegerField('Page Count')
    is_hardcover = BooleanField('Is Hardcover?')
    submit_button = SubmitField('Contribute')