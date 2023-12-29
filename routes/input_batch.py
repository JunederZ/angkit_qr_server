from flask import request, make_response, current_app
from playhouse.shortcuts import model_to_dict
from flasgger import swag_from
from database.models import *
from peewee import *
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import random
import string
import segno
import uuid
import os
import io


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
        qrpath = generateQrCode(idBatch)
        data = BatchUnggas.create(
            id=idBatch,
            berat_rt_sample=datas.get('beratRata'),
            distributor=datas.get('distributor'),
            jenis_ternak=datas.get('jenisTernak'),
            nama=datas.get('nama'),
            spesies=datas.get('spesies'),
            peternak=datas.get('peternak'),
            tgl_kemas=datas.get('tanggalKemas'),
            tgl_mulai=datas.get('tanggalMulai'),
            tgl_potong=datas.get('tanggalPotong'),
            qrcode=qrpath
        )
        data.save()
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


def generateQrCode(datas):
    qrcode = segno.make(datas, micro=False)
    out = io.BytesIO()
    qrname = uuid.uuid4().hex + ".png"
    saveto = os.path.join(current_app.config['QR_FOLDER'], qrname)
    qrcode.save(out, kind='png', scale=10)
    out.seek(0)
    img = Image.open(out)
    text = ImageDraw.Draw(img)
    myFont = ImageFont.truetype("../database/G_ari_bd.TTF", 30)
    text.text((95, 250), datas, font=myFont)
    img.save(saveto)
    return qrname
