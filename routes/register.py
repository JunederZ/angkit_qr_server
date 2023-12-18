from flask import request, make_response
import models.PeternakModel as PeternakModel
from database.db_util import DBUtil
from flasgger import swag_from


@swag_from('../docs/Register.yml')
def register():
    datas = request.get_json()
    username = ''
    password = ''
    role = ''

    try:
        username = datas['username']
        password = datas['password']
        role = datas['role']

    except KeyError as e:
        return make_response({
            'status': 'error',
            'message': f"can't find data [{e}]",
        }, 403)

    res = DBUtil().add_user(username, password, role)
    if res != "success":
        return make_response({
            'status': 'error',
            'message': res,
        }, 404)

    return make_response({
        'status': 'ok',
    }, 201)
