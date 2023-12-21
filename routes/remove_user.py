from flask import request, make_response
from argon2 import PasswordHasher
import argon2
from database.models import *
from flasgger import swag_from


@swag_from('../docs/RemoveUser.yml')
def remove_user():
    json = request.get_json()
    username = json.get('username')

    user = Users.select().where(Users.username == username)
    if user.exists():
        user.first().delete_instance()
        return make_response({
            'status': 'ok',
            'message': f'User {username} has been removed'
        }, 204)
    return make_response({
        'status': 'error',
        'message': 'not found'
    }, 404)
