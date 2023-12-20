from flask import request, make_response
from database.models import *
from peewee import *
from flasgger import swag_from


@swag_from('../docs/AddPeternakan.yml')
def addPeternakan():
    datas = request.get_json()

    try:
        if datas['id'] and datas['lokasi'] and datas['nama'] and datas['username']:
            Peternakan.insert(datas).execute()
    except IntegrityError as e:
        if "already exists" in f"{e}":
            return make_response({
                'status': 'error',
                'message': f"id {datas['id']} already exists.",
            }, 409)
        elif "violates foreign key" in f"{e}":
            return make_response({
                'status': 'error',
                'message': f"not found foreign key {datas['username']}.",
            }, 403)
        else:
            return make_response({
                'status': 'error',
                'message': f"{e}.",
            }, 403)
    except KeyError as e:
        return make_response({
            'status': 'error',
            'message': f"can't find data [{e}].",
        }, 403)
    except ValueError as e:
        return make_response({
            'status': 'error',
            'message': f"{e}.",
        }, 403)

    return make_response({
        'status': 'ok',
    }, 201)
