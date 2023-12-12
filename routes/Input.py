from flask import request, make_response
import models.BatchModel

def inputBatch():
    data = request.get_json()



    return make_response({
        'status': 'ok',
        'data': data,
    }, 200)