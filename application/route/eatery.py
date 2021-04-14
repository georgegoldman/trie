from flask import Blueprint

eat = Blueprint('eat',__name__)

@eat.route('/eat')
def eatery():
    return 'hi'