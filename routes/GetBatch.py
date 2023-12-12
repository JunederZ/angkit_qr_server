from flask import request, make_response
from database.db_util import DBUtil


def getBatch():

    json = request.get_json()
    if not json.get("id"):
        return make_response({
                'status': 'error',
                'message': "Please provide a valid ID"
            }, 200)
    data = DBUtil().get_batch_by_id(json['id'])
    if data == "not found":
        return make_response({
            'status': 'error',
            'message': "Please provide a valid ID"
        }, 200)
    return make_response({
        "status": "ok",
        'data': data.getData(),
    }, 200)
