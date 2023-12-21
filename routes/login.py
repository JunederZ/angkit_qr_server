from flask import request, make_response
from argon2 import PasswordHasher
import argon2
from database.models import *
from flasgger import swag_from

@swag_from('../docs/Login.yml')
def login():
    json = request.get_json()
    username = json.get('username')
    password = json.get('password')

    user = Users.select().where(Users.username == username)
    userObject = user.first()
    try:
        if user.exists() and PasswordHasher().verify(password=password, hash=userObject.password):
            return make_response({
                'status': 'ok',
                'username': userObject.username,
                'role': userObject.role,
            }, 200)
    except argon2.exceptions.VerifyMismatchError:
        return make_response({
            'status': 'error',
            'message': 'Wrong password'
        }, 401)
    return make_response({
        'status': 'error',
        'message': 'not found'
    }, 404)
