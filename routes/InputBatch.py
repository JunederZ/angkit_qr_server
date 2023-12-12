from flask import request, make_response
import models.BatchModel as BatchModel
from database.db_util import DBUtil


def inputBatch():
    datas = request.get_json()

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

    return make_response({
        'status': 'ok',
    }, 200)
