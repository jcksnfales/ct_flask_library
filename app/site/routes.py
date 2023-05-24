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

@site.route('/contribute', methods=['GET','POST'])
def contribute():
    # check if there is a user currently logged in
    if current_user.is_authenticated:
        # if user is logged in, instantiate the form and wait for POST
        form = BookContributionForm()

        try:
            if request.method == 'POST' and form.validate_on_submit():
                title = form.title.data
                isbn = form.title.data
                author = form.author.data
                page_count = form.page_count.data
                is_hardcover = form.is_hardcover.data

                new_book = Book(current_user.token, isbn, title, author, page_count, is_hardcover)
                db.session.add(new_book)
                db.session.commit()

                flash(f'Successfully added the book "{title}"', category='contribute-success')
                return redirect('/contribute')
        except:
            raise Exception('Invalid Form Data')
        
        # until POST, direct user to the contribution form
        return render_template('contribute.html', form=form)
    else:
        # otherwise, flash a warning and redirect them to the signin page
        flash('You must be logged in to contribute books.', category='access-profile-failed')
        return redirect('/signin')
    
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
