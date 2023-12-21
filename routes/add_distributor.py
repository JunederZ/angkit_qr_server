from flask import request, make_response
from flasgger import swag_from
from playhouse.shortcuts import model_to_dict, dict_to_model
from database.models import *
from peewee import *
import uuid


@swag_from('../docs/AddDistributor.yml')
def add_distributor():
    try:
        datas = request.get_json()
    except Exception as e:
        return make_response({
            'status': 'error',
            'message': f"broken json [{e}]",
        }, 400)
    data = None
    try:
        if datas['lokasi'] and datas['nama'] and datas['username']:
            data = Distributor.create(
                nama=datas['nama'],
                lokasi=datas['lokasi'],
                id=uuid.uuid4().hex,
                username=datas['username'],
            )
            data.save()
    except IntegrityError as e:
        if "violates foreign key" in f"{e}":
            return make_response({
                'status': 'error',
                'message': f"username {datas['username']} doesn't exist",
            }, 404)
        else:
            return make_response({
                'status': 'error',
                'message': f"{e}.",
            }, 400)
    except KeyError as e:
        return make_response({
            'status': 'error',
            'message': f"Missing field [{e}].",
        }, 400)

    return make_response({
        'status': 'ok',
        'data': model_to_dict(data, exclude=[Distributor.user])
    }, 201)
