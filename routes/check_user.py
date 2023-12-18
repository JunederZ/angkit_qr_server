from flask import request, make_response
from database.db_util import DBUtil
from flasgger import swag_from


@swag_from('../docs/CheckUser.yml')
def check_user():
    json = request.get_json()
    if not json.get("username"):
        return make_response({
            'status': 'error',
            'message': "Please provide the username"
        }, 400)
    data = DBUtil.check_user_exists(json['username'])
    if data:
        return make_response({
            'status': 'error',
            'available': "Username already exists"
        }, 404)
    return make_response({
        "status": "ok",
        'data': "Username available"
    }, 200)
