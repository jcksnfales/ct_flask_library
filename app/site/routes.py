from flask import Blueprint, render_template, request, redirect, flash
from flask_login import current_user
from models import Book, book_schema, books_schema, db
from forms import BookContributionForm

site = Blueprint('site', __name__, template_folder='site_templates')

def reformat_isbns(books):
    for book_num in range(len(books)):
        isbn = str(books[book_num]['isbn'])
        books[book_num]['isbn'] = f'{isbn[0:3]}-{isbn[3]}-{isbn[4:6]}-{isbn[6:12]}-{isbn[12]}'
    return books

# LANDING PAGE
@site.route('/')
def landing():
    return render_template('index.html')
    
# BOOK CATALOG
@site.route('/books')
def book_catalog():
    # query database for all books
    queried_books = Book.query.all()
    # reformat books_json's ISBNs to add hyphens
    books_json = reformat_isbns(books_schema.dump(queried_books))
    # then direct user to catalog, passing in found books
    return render_template('catalog.html', books=queried_books, books_json=books_json)

# CONTRIBUTION FORM
@site.route('/contribute', methods=['GET','POST'])
def contribute():
    # check if there is a user currently logged in
    if current_user.is_authenticated:
        # if user is logged in, instantiate the form and wait for POST
        form = BookContributionForm()

        try:
            if request.method == 'POST' and form.validate_on_submit():
                title = str(form.title.data)
                isbn = int(form.isbn.data)
                author = str(form.author.data)
                page_count = int(form.page_count.data)
                is_hardcover = bool(form.is_hardcover.data)

                new_book = Book(current_user.token, isbn, title, author, page_count, is_hardcover)
                db.session.add(new_book)
                db.session.commit()

                flash(f'Successfully added the book "{title}"', category='contribute-success')
                return redirect('/contribute')
        except:
            raise Exception(f'Invalid Form Data')
        
        # until POST, direct user to the contribution form
        return render_template('contribute.html', form=form)
    else:
        # otherwise, flash a warning and redirect them to the signin page
        flash('You must be logged in to contribute books.', category='access-contribute-failed')
        return redirect('/signin')

# PROFILE
@site.route('/profile')
def profile():
    # check if there is a user currently logged in
    if current_user.is_authenticated:
        # if user is logged in, query database for books contributed by this user
        queried_books = Book.query.filter_by(contributor_token=current_user.token).all()
        # reformat books_json's ISBNs to add hyphens
        books_json = reformat_isbns(books_schema.dump(queried_books))
        # then direct user to profile, passing in found books
        return render_template('profile.html', books=queried_books, books_json=books_json)
    else:
        # otherwise, flash a warning and redirect them to the signin page
        flash('You must be logged in to access the profile page.', category='access-profile-failed')
        return redirect('/signin')
