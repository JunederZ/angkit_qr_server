from flask import request, make_response
import models.DistributorModel as DistributorModel
from database.db_util import DBUtil


def addDistributor():
    datas = request.get_json()

    try:
        disModel = DistributorModel.DistributorModel(
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
        }, 404)

    responses = DBUtil().add_distributor(disModel)
    if responses != "ok":
        return make_response({
            'status': 'error',
            'message': responses,
        }, 404)

    return make_response({
        'status': 'ok',
    }, 200)
