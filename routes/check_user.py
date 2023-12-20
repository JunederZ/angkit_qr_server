from flask import request, make_response
from flasgger import swag_from
from database.models import *

@swag_from('../docs/CheckUser.yml')
def check_user():
    json = request.get_json()
    if not json.get("username"):
        return make_response({
            'status': 'error',
            'message': "Please provide the username"
        }, 403)
    data = Users.select().where(Users.username == json.get('username'))
    if data.exists():
        return make_response({
            'status': 'error',
            'available': "Username already exists"
        }, 409)
    return make_response({
        "status": "ok",
        'data': "Username available"
    }, 200)
