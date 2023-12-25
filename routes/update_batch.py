from flask import request, make_response
from flasgger import swag_from
from playhouse.shortcuts import model_to_dict
from database.models import *

@swag_from('../docs/UpdateBatch.yml')
def update_batch():
    try:
        datas = request.get_json()
    except Exception as e:
        return make_response({
            'status': 'error',
            'message': f"broken json [{e}]",
        }, 400)
    if not datas.get("id"):
        return make_response({
            'status': 'error',
            'message': "Please provide the ID"
        }, 400)
    data = BatchUnggas.select().where(BatchUnggas.id == datas.get("id"))
    if not data.exists():
        return make_response({
            'status': 'error',
            'message': "Batch with that ID doesn't exists"
        }, 404)

    fields_to_update = {
        'berat_rt_sample': datas.get('beratRata'),
        'distributor': datas.get('distributor'),
        'jenis_ternak': datas.get('jenisTernak'),
        'peternak': datas.get('peternak'),
        'tgl_kemas': datas.get('tanggalKemas'),
        'tgl_mulai': datas.get('tanggalMulai'),
        'tgl_potong': datas.get('tanggalPotong')
    }
    fields_to_update = {k: v for k, v in fields_to_update.items() if v is not None}

    query = BatchUnggas.update(**fields_to_update).where(BatchUnggas.id == datas.get("id"))
    query.execute()
    return make_response({
        "status": "ok",
        'data': model_to_dict(BatchUnggas.select().where(BatchUnggas.id == datas.get("id")).get(), exclude=[Peternakan.user, Distributor.user]),
    }, 200)
