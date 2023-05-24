from flask import Blueprint, render_template, redirect
from flask_login import current_user
from models import Book, book_schema, books_schema

site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def landing():
    return render_template('index.html')

@site.route('/profile')
def profile():
    # check if there is a user currently logged in
    if current_user.is_authenticated:
        # if user is logged in, direct them to their profile
        return render_template('profile.html')
    else:
        # otherwise, redirect them to the landing page
        return redirect('/')