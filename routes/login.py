from flask import request, make_response
from argon2 import PasswordHasher
import argon2
from playhouse.shortcuts import model_to_dict

from database.models import *
from flasgger import swag_from

@swag_from('../docs/Login.yml')
def login():
    json = request.get_json()
    username = json.get('username')
    password = json.get('password')

    user = Users.select().where(Users.username == username)
    userObject = user.first()
    user_res = model_to_dict(userObject, backrefs=True)
    try:
        if user.exists() and PasswordHasher().verify(password=password, hash=userObject.password):
            return make_response({
                'status': 'ok',
                'user': user_res,
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
