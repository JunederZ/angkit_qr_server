from flask import request, make_response
from database.db_util import DBUtil

def login():
    json = request.get_json()
    username = json.get('username')
    password = json.get('password')

    user = DBUtil().user_login(username, password)
    if user != 'User not exists' and user != 'wrong password':
        print(user)
        return make_response({
            'status': 'ok',
            'username': user[0],
            'role': user[2],
        }, 200)
    return make_response({
        'status': user,
    }, 200)
