from flask import request, make_response
import models.BatchModel as BatchModel
from database.db_util import DBUtil


def inputBatch():
    datas = request.get_json()

    try:
        batchModel = BatchModel.BatchModel(
            (
                datas['id'],
                datas['jenisTernak'],
                datas['peternak'],
                datas['distributor'],
                datas['beratRata'],
                datas['tanggalMulai'],
                datas['tanggalPotong'],
                datas['tanggalKemas'],
            )
        )
    except KeyError as e:
        return make_response({
            'status': 'error',
            'message': f"can't find data [{e}]",
        }, 200)

    responses = DBUtil().input_batch(batchModel)
    if responses != "ok":
        return make_response({
            'status': 'error',
            'message': responses,
        }, 200)

    return make_response({
        'status': 'ok',
    }, 200)
