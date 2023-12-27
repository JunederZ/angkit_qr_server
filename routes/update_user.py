from flask import request, make_response
from flasgger import swag_from
from playhouse.shortcuts import model_to_dict
from database.models import *
from argon2 import PasswordHasher
import argon2


@swag_from('../docs/UpdateUser.yml')
def update_user():
    try:
        datas = request.get_json()
    except Exception as e:
        return make_response({
            'status': 'error',
            'message': f"broken json [{e}]",
        }, 400)
    if not datas.get("username"):
        return make_response({
            'status': 'error',
            'message': "Please provide the ID"
        }, 400)
    data = Users.select().where(Users.username == datas.get("username"))
    if not data.exists():
        return make_response({
            'status': 'error',
            'message': "user with that username doesn't exists"
        }, 404)

    role = "Peternakan" if data.get().role == "Peternakan" else "Distributor"
    pw = PasswordHasher().hash(datas.get("password")) if datas.get("password") is not None else None
    fields_to_update = {
        'username': datas.get("username"),
        'password': pw,
    }
    fields_to_update_role = {
        'lokasi': datas.get("lokasi"),
        'nama': datas.get("nama"),
    }
    fields_to_update = {k: v for k, v in fields_to_update.items() if v is not None}
    fields_to_update_role = {k: v for k, v in fields_to_update_role.items() if v is not None}

    query = Users.update(**fields_to_update).where(Users.username == datas.get("username"))
    if role == "Peternakan":
        query_role = Peternakan.update(**fields_to_update_role).where(Peternakan.user == datas.get("username"))
    else:
        query_role = Distributor.update(**fields_to_update_role).where(Distributor.user == datas.get("username"))
    query.execute()
    query_role.execute()
    return make_response({
        "status": "ok",
        'data': model_to_dict(Users.select().where(Users.username == datas.get("username")).get(), exclude=[Users.password], max_depth=1, backrefs=True),
    }, 200)
