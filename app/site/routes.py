from flask import Blueprint, render_template, request, redirect, flash
from flask_login import current_user
from models import Book, book_schema, books_schema, db
from forms import BookContributionForm

site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def landing():
    return render_template('index.html')
    
@site.route('/books')
def book_catalog():
    # query database for books
    queried_books = Book.query.all()
    return render_template('catalog.html', books=queried_books, books_json=books_schema.dump(queried_books))

@site.route('/profile')
def profile():
    # check if there is a user currently logged in
    if current_user.is_authenticated:
        # if user is logged in, direct them to their profile
        return render_template('profile.html')
    else:
        # otherwise, flash a warning and redirect them to the signin page
        flash('You must be logged in to access the profile page.', category='access-contribute-failed')
        return redirect('/signin')
