from flask import request, make_response
from flasgger import swag_from
from argon2 import PasswordHasher
from database.models import *


@swag_from('../docs/Register.yml')
def register():
    try:
        datas = request.get_json()
    except Exception as e:
        return make_response({
            'status': 'error',
            'message': f"broken json [{e}]",
        }, 400)

    try:
        if Users.select().where(Users.username == datas['username']).exists():
            return make_response({
                'status': 'error',
                'message': 'user already exists',
            }, 409)
        pw = PasswordHasher()
        data = Users.create(
            username=datas['username'],
            password=pw.hash(datas['password']),
            role=datas['role']
        )
        data.save()
    except KeyError as e:
        return make_response({
            'status': 'error',
            'message': f"Missing Field [{e}]",
        }, 403)
    return make_response({
        'status': 'ok',
    }, 201)
