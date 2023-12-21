from flask import request, make_response
from flasgger import swag_from
from playhouse.shortcuts import model_to_dict
import random
import string
from database.models import *
from peewee import *

@swag_from('../docs/InputBatch.yml')
def inputBatch():
    try:
        datas = request.get_json()
    except Exception as e:
        return make_response({
            'status': 'error',
            'message': f"broken json [{e}]",
        }, 400)
    try:
        existing_ids = set(BatchUnggas.select(BatchUnggas.id).tuples())
        while True:
            idBatch = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=6))
            if idBatch not in existing_ids:
                break
        data = BatchUnggas.create(
            id=idBatch,
            berat_rt_sample=datas['beratRata'],
            distributor=datas['distributor'],
            jenis_ternak=datas['jenisTernak'],
            peternak=datas['peternak'],
            tgl_kemas=datas['tanggalKemas'],
            tgl_mulai=datas['tanggalMulai'],
            tgl_potong=datas['tanggalPotong']
        )
        data.save()
    except KeyError as e:
        return make_response({
            'status': 'error',
            'message': f"Missing field [{e}]",
        }, 400)
    except IntegrityError as e:
        if "violates foreign key" in f"{e}":
            return make_response({
                'status': 'error',
                'message': f"{e}]",
            }, 404)
        else:
            return make_response({
                'status': 'error',
                'message': f"{e}.",
            }, 400)

    return make_response({
        'status': 'ok',
        'data': model_to_dict(data, exclude=[Peternakan.user, Distributor.user])
    }, 201)
