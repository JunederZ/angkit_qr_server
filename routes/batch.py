from flask import request, make_response, current_app
from database.models import *
from flasgger import swag_from
from peewee import *
import uuid
from playhouse.shortcuts import model_to_dict, dict_to_model


@swag_from('../docs/GetAllBatch.yml')
def get_all_batch():
    try:
        batches = BatchUnggas.select()
        batches = [model_to_dict(batch, exclude=[Distributor.user, Peternakan.user, BatchImages.id], backrefs=True) for batch in batches]
    except DoesNotExist:
        return make_response({
            "status": "error",
            'msg': 'no batches',
        }, 404)
    return make_response({
        "status": "ok",
        'batches': batches,
    }, 200)


# @swag_from('../docs/GetBatch.yml')
def get_batch_by_distributor():
    json = request.get_json()
    if not json.get("distributor_id"):
        return make_response({
            'status': 'error',
            'message': "Please provide the field `distributor_id`"
        }, 400)
    try:
        batches = BatchUnggas.select().where(BatchUnggas.distributor == json.get("distributor_id"))
        batches = [model_to_dict(i, exclude=[Distributor.user, Peternakan.user], backrefs=True) for i in batches]

    except DoesNotExist:
        return make_response({
            "status": "error",
            'msg': 'no batches',
        }, 404)
    return make_response({
        "status": "ok",
        'batches': batches,
    }, 200)


# @swag_from('../docs/GetBatch.yml')
def get_batch_by_farm():
    json = request.get_json()
    if not json.get("farm_id"):
        return make_response({
            'status': 'error',
            'message': "Please provide the field `farm_id`"
        }, 400)
    try:
        batches = BatchUnggas.select().where(BatchUnggas.peternak == json.get("farm_id"))
        batches = [model_to_dict(i, exclude=[Distributor.user, Peternakan.user], backrefs=True) for i in batches]

    except DoesNotExist:
        return make_response({
            "status": "error",
            'msg': 'no batches',
        }, 404)
    return make_response({
        "status": "ok",
        'batches': batches,
    }, 200)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def add_image():
    batch_id = request.form.get('batch_id')
    if not batch_id:
        return make_response({
            "status": "no batch_id provided"
        }, 400)
    if 'file' not in request.files:
        return make_response({
            "status": "no file provided"
        }, 400)

    file = request.files['file']

    if not allowed_file(file.filename):
        return make_response({
            "status": "file extension must be either png or jpg"
        }, 400)

    filename = uuid.uuid4().hex + '.' + file.filename.rsplit('.', 1)[1].lower()
    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
    batch_image = BatchImages(filename=filename, batch_id=batch_id)
    try:
        batch_image.save()

    except IntegrityError as e:
        return make_response({
            "status": "error",
            "msg": str(e)
        }, 400)

    return make_response({
        "status": "ok",
        "data": model_to_dict(batch_image, recurse=False, )
    }, 201)

