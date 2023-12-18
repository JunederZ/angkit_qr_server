from flask import request, make_response
from database.models import *
from flasgger import swag_from
import uuid
from playhouse.shortcuts import model_to_dict, dict_to_model


# @swag_from('../docs/GetBatch.yml')
def get_all_batch():
    try:
        batches = BatchUnggas.select()
        batches = [model_to_dict(batch, exclude=[Distributor.user, Peternakan.user]) for batch in batches]
    except DoesNotExist:
        return make_response({
            "status": "error",
            'msg': 'no batches',
        }, 404)
    return make_response({
        "status": "ok",
        'batches': batches,
    }, 200)


# @swag_from('../docs/GetBatch.yml')
def get_batch_by_distributor():
    json = request.get_json()
    if not json.get("distributor_id"):
        return make_response({
            'status': 'error',
            'message': "Please provide the field `distributor_id`"
        }, 400)
    try:
        batches = BatchUnggas.select().where(BatchUnggas.distributor == json.get("distributor_id"))
        batches = [model_to_dict(i, exclude=[Distributor.user, Peternakan.user]) for i in batches]

    except DoesNotExist:
        return make_response({
            "status": "error",
            'msg': 'no batches',
        }, 404)
    return make_response({
        "status": "ok",
        'batches': batches,
    }, 200)


# @swag_from('../docs/GetBatch.yml')
def get_batch_by_farm():
    json = request.get_json()
    if not json.get("farm_id"):
        return make_response({
            'status': 'error',
            'message': "Please provide the field `farm_id`"
        }, 400)
    try:
        batches = BatchUnggas.select().where(BatchUnggas.peternak == json.get("farm_id"))
        batches = [model_to_dict(i, exclude=[Distributor.user, Peternakan.user]) for i in batches]

    except DoesNotExist:
        return make_response({
            "status": "error",
            'msg': 'no batches',
        }, 404)
    return make_response({
        "status": "ok",
        'batches': batches,
    }, 200)

def add_dist():
    json = request.get_json()
    try:
        dist = dict_to_model(Distributor, {
            "id": uuid.uuid4().hex,
            "username": json.get("username"),
            "nama": json.get("nama"),
            "lokasi": json.get("lokasi"),
        })
        dist.save()
    except KeyError as e:
        return make_response({
            'status': 'error',
            'message': f"Required field `{e}` is not present",
        }, 403)



