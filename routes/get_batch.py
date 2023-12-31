from flask import request, make_response
from database.models import *
from playhouse.shortcuts import model_to_dict
from flasgger import swag_from


@swag_from('../docs/GetBatch.yml')
def getBatch():
    json = request.get_json()
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
        'data': model_to_dict(data.get(), exclude=[Peternakan.user, Distributor.user]),
    }, 200)
