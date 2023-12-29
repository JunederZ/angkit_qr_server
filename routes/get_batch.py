from flasgger import swag_from
from flask import request, make_response
from playhouse.shortcuts import model_to_dict
from database.models import *


@swag_from('../docs/GetBatch.yml')
def getBatch(batchID):
    if not batchID:
        return make_response({
            'status': 'error',
            'message': "Please provide the ID"
        }, 400)
    data = BatchUnggas.select().where(BatchUnggas.id == batchID)
    if not data.exists():
        return make_response({
            'status': 'error',
            'message': "Batch with that ID doesn't exists"
        }, 404)
    return make_response({
        "status": "ok",
        'data': model_to_dict(data.get(), exclude=[Peternakan.user, Distributor.user], backrefs=True),
    }, 200)
