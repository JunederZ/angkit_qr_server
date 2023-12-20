from flask import request, make_response
from flasgger import swag_from
from database.models import *


@swag_from('../docs/Register.yml')
def register():
    datas = request.get_json()

    try:
        if Users.select().where(Users.username == datas['username']).exists():
            return make_response({
                'status': 'error',
                'message': 'user already exists',
            }, 409)

        data = Users.create(
            username=datas['username'],
            password=datas['password'],
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
