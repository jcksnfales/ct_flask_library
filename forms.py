from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

# AUTH LOGIN FORM
class UserLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message='Please enter a valid email address.')])
    password = PasswordField('Password', validators=[DataRequired()])
    submit_button = SubmitField('Submit')

# AUTH REGISTRATION FORM
class UserRegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message='Please enter a valid email address.')])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password_confirm', message='Passwords must match.')])
    password_confirm = PasswordField('Confirm Password')
    submit_button = SubmitField('Submit')

# BOOK CONTRIBUTION FORM
# define custom validator for checking if ISBN is valid
def ValidISBN():
    message = "ISBN must be a valid 13-digit integer"

    def validator_func(form, field):
        if len(str(field.data)) != 13:
            raise ValidationError(message)

    return validator_func

# the form object itself
class BookContributionForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    isbn = IntegerField('ISBN', validators=[ValidISBN()])
    author = StringField('Author Name')
    page_count = IntegerField('Page Count')
    is_hardcover = BooleanField('Is Hardcover?')
    submit_button = SubmitField('Contribute')