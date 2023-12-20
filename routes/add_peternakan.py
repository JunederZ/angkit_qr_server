from flask import request, make_response
from playhouse.shortcuts import model_to_dict, dict_to_model
import uuid
from database.models import *
from peewee import *
from flasgger import swag_from


@swag_from('../docs/AddPeternakan.yml')
def add_peternakan():
    datas = request.get_json()
    data = None
    try:
        if datas['lokasi'] and datas['nama'] and datas['username']:
            data = Peternakan.create(
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
                'message': f"foreign key [{datas['username']}] not found.",
            }, 404)
        else:
            return make_response({
                'status': 'error',
                'message': f"{e}.",
            }, 400)
    except KeyError as e:
        return make_response({
            'status': 'error',
            'message': f"can't find data [{e}].",
        }, 400)

    return make_response({
        'status': 'ok',
        'data': model_to_dict(data, exclude=[Peternakan.user])
    }, 201)