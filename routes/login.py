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
    site_id = ''
    if userObject.role == 'Peternakan':
        site_id = Peternakan.select().where(Peternakan.user == userObject.username).first().id
    elif userObject.role == 'Distributor':
        site_id = Distributor.select().where(Distributor.user == userObject.username).first().id
    try:
        if user.exists() and PasswordHasher().verify(password=password, hash=userObject.password):
            return make_response({
                'status': 'ok',
                'user': userObject.username,
                'role': userObject.role,
                'id': site_id,
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
