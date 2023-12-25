from flasgger import swag_from
from flask import request, make_response
from playhouse.shortcuts import model_to_dict
from database.models import *


@swag_from('../docs/GetBatch.yml')
def getBatch():
    try:
        json = request.get_json()
    except Exception as e:
        return make_response({
            'status': 'error',
            'message': f"broken json [{e}]",
        }, 400)
    if not json.get("id"):
        return make_response({
            'status': 'error',
            'message': "Please provide the ID"
        }, 400)
    data = BatchUnggas.select().where(BatchUnggas.id == json.get("id"))
    if not data.exists():
        return make_response({
            'status': 'error',
            'message': "Batch with that ID doesn't exists"
        }, 404)
    return make_response({
        "status": "ok",
        'data': model_to_dict(data.get(), exclude=[Peternakan.user, Distributor.user], backrefs=True),
    }, 200)
