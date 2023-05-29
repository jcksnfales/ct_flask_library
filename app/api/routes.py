from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Book, book_schema, books_schema

api = Blueprint('api',__name__, url_prefix='/api')

# ADD NEW BOOK
@api.route('/books', methods=['POST'])
@token_required
def add_book(current_user_token):
    title = request.json['title']
    isbn = request.json['isbn']
    author = request.json['author']
    page_count = request.json['page_count']
    is_hardcover = request.json['is_hardcover']

    new_book = Book(current_user_token.token, isbn, title, author, page_count, is_hardcover)

    db.session.add(new_book)
    db.session.commit()

    return jsonify(book_schema.dump(new_book))

# GET ALL BOOKS
@api.route('/books', methods=['GET'])
@api.route('/books/all', methods=['GET'])
@token_required
def get_all_books(current_user_token):
    # query all books
    all_books = books_schema.dump(Book.query.all())
    # iterate through books, removing access tokens that do not belong to the current user
    for book_num in range(len(all_books)):
        if all_books[book_num]['contributor_token'] != current_user_token.token:
            all_books[book_num]['contributor_token'] = 'DIFFERENT USER'
    # return filtered list of all books  
    return jsonify(all_books)

# GET ALL BOOKS CONTRIBUTED BY USER
@api.route('/books/mine', methods=['GET'])
@token_required
def get_user_books(current_user_token):
    user_books = Book.query.filter_by(contributor_token=current_user_token.token).all()
    return jsonify(books_schema.dump(user_books)) if user_books else jsonify({'message': 'You have not added any books. Add one through the website or with a POST request and a JSON string like the given example.', 'example':{'title':'Book Title', 'isbn':1001101000001, 'author':'Author Name', 'page_count':0, 'is_hardcover':False}})

# GET BOOK BY ID
@api.route('/books/<id>', methods=['GET'])
@token_required
def get_book_by_id(current_user_token, id):
    # find book by id
    current_book = Book.query.get(id)
    # check book's contributor_token against the current user's token
    if current_user_token.token == current_book.contributor_token:
        # if user tokens match, return book's data
        return jsonify(book_schema.dump(current_book))
    else:
        # if user tokens do not match, return an error message
        return jsonify({'message': f'Given book {id} does not belong to given access token'})

# UPDATE BOOK BY ID
@api.route('/books/<id>', methods=['POST','PUT'])
@token_required
def update_book_by_id(current_user_token, id):
    # find book by id
    updated_book = Book.query.get(id)
    # check book's contributor_token against the current user's token
    if current_user_token.token == updated_book.contributor_token:
        # if user tokens match, update book's data
        updated_book.title = request.json['title']
        updated_book.isbn = request.json['isbn']
        updated_book.author = request.json['author']
        updated_book.page_count = request.json['page_count']
        updated_book.is_hardcover = request.json['is_hardcover']
        return jsonify(book_schema.dump(updated_book))
    else:
        # if user tokens do not match, return an error message
        return jsonify({'message': f'Given book {id} does not belong to given access token'})

# DELETE BOOK
@api.route('/books/<id>', methods=['DELETE'])
@token_required
def delete_book_by_id(current_user_token, id):
    # find book by id
    deleted_book = Book.query.get(id)
    # check book's contributor_token against the current user's token
    if current_user_token.token == deleted_book.contributor_token:
        # if user tokens match, delete the book
        db.session.delete(deleted_book)
        db.session.commit()
        return jsonify(book_schema.dump(deleted_book))
    else:
        # if user tokens do not match, return an error message
        return jsonify({'message': f'Given book {id} does not belong to given access token'})