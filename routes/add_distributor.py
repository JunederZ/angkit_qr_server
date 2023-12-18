from flask import request, make_response
import models.distributor_model as DistributorModel
from database.db_util import DBUtil
from flasgger import swag_from


@swag_from('../docs/AddDistributor.yml')
def add_distributor():
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
        }, 403)

    return make_response({
        'status': 'ok',
    }, 200)
