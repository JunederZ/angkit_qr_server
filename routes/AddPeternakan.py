from flask import request, make_response
import models.PeternakModel as PeternakModel
from database.db_util import DBUtil


def addPeternakan():
    datas = request.get_json()

    try:
        peternakModel = PeternakModel.PeternakModel(
            (
                datas['nama'],
                datas['lokasi'],
                datas['id'],
            )
        )
    except KeyError as e:
        return make_response({
            'status': 'error',
            'message': f"can't find data [{e}]",
        }, 200)

    responses = DBUtil().add_peternak(peternakModel)
    if responses != "ok":
        return make_response({
            'status': 'error',
            'message': responses,
        }, 200)

    return make_response({
        'status': 'ok',
    }, 200)
