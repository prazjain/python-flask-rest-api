from flask import Flask, jsonify, request, Response
import json
from settings import *
from BookModel import Book
from UserModel import User
import datetime
import jwt
from functools import wraps

DEFAULT_PAGE_LIMIT = 3
app.config['SECRET_KEY'] = 'TEST_ONLY'


def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args.get('token')
        try:
            jwt.decode(token, app.config['SECRET_KEY'])
            return f(*args, **kwargs)
        except:
            return jsonify({'error': 'Need a valid token to view this page'}), 401

    return wrapper


@app.route('/login', methods=['POST'])
def get_token():
    request_data = request.get_json()
    if 'username' not in request_data or 'password' not in request_data:
        return Response('', 401, mimetype='application/json')
    username = str(request_data['username'])
    password = str(request_data['password'])
    if User.username_password_match(username, password):
        expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=60 * 5)
        token = jwt.encode({'exp': expiration_date}, app.config['SECRET_KEY'], algorithm='HS256')
        return token
    else:
        return Response('', 401, mimetype='application/json')


# GET /books?token=asasdfkkjhsgdkjfaghskdjhfg
@app.route('/books')
@token_required
def get_books():
    return jsonify({'books': Book.get_all_books()})


# GET /books/page/<int:page_number>
# /books/page/1?limit=100
@app.route('/books/page/<int:page_number>')
@token_required
def get_paginated_books(page_number):
    print(type(request.args.get('limit')))
    LIMIT = request.args.get('limit', DEFAULT_PAGE_LIMIT, int)
    start_index = page_number * LIMIT
    end_index = page_number * LIMIT
    print(start_index)
    print(end_index)
    return jsonify({'books': Book.get_all_books()[start_index:end_index]})


def validBookObject(bookObject):
    if 'name' in bookObject and 'price' in bookObject and 'isbn' in bookObject:
        return True
    else:
        return False


@app.route('/books', methods=['POST'])
@token_required
def add_book():
    request_data = request.get_json()
    if validBookObject(request_data):
        Book.add_book(request_data['name'], request_data['price'], request_data['isbn'], )
        response = Response('', 201, mimetype='application/json')
        response.headers['Location'] = '/books/' + str(request_data['isbn'])
        return response
    else:
        invalidBookObjectErrorMsg = {
            "error": "Invalid book object passed in request",
            "helpString": "Data passed in similar to this { 'name' : 'bookName' , 'price' : 2.99, 'isbn' : 1234232435 }"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
        return response


@app.route('/books/<int:isbn>')
@token_required
def get_book_by_isbn(isbn):
    return_value = Book.get_book(isbn)
    return jsonify(return_value)


def valid_put_request_data(request_data):
    if 'name' in request_data and 'price' in request_data:
        return True
    else:
        return False


@app.route('/books/<int:isbn>', methods=['PUT'])
@token_required
def replace_book(isbn):
    request_data = request.get_json()
    if not valid_put_request_data(request_data):
        invalidBookObjectErrorMsg = {
            "error": "Invalid book object passed in request",
            "helpString": "Data passed in similar to this { 'name' : 'bookName' , 'price' : 2.99 }"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
        return response

    Book.replace_book(isbn, request_data['name'], request_data['price'])
    response = Response('', 201, mimetype='application/json')
    response.headers['Location'] = '/books/' + str(isbn)
    return response


def valid_patch_request_data(request_data):
    if 'name' in request_data or 'price' in request_data:
        return True
    else:
        return False


@app.route('/books/<int:isbn>', methods=['PATCH'])
@token_required
def update_book(isbn):
    request_data = request.get_json()
    if not valid_patch_request_data(request_data):
        invalidBookObjectErrorMsg = {
            "error": "Invalid book object passed in request"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
        return response

    if 'name' in request_data:
        Book.update_book_name(isbn, request_data['name'])
    if 'price' in request_data:
        Book.update_book_price(isbn, request_data['price'])

    response = Response('', 201, mimetype='application/json')
    response.headers['Location'] = '/books/' + str(isbn)
    return response


@app.route('/books/<int:isbn>', methods=['DELETE'])
@token_required
def delete_book(isbn):
    if Book.delete_book(isbn):
        return Response('', status=204)

    invalidIsbnErrorMsg = {
        "error": "Book with Isbn number is not found, please try with valid isbn"
    }
    response = Response(json.dumps(invalidIsbnErrorMsg), status=404, mimetype='application/json')
    return response


app.run(port=5000)
