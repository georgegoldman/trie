from flask import Blueprint, render_template, request

eat = Blueprint('eat',__name__)

@eat.route('/eat')
def eatery():
    return 'hi'

@eat.route('/register', methods=['GET'])
def register_get():
    return render_template('register.html')

@eat.route('/register', methods=['POST'])
def register_post():
    body  = request.form
    return body