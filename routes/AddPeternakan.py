from flask import request, make_response
import models.PeternakModel as PeternakModel
from database.db_util import DBUtil


def addPeternakan():
    """
    Add new peternakan to the database.
    ---
    tags:
      - Peternakan
    parameters:
      - name: Body
        type: json
        in: body
        required: true
        schema:
          $ref: '#/definitions/example'

    definitions:
      example:
        type: string
        properties:
          nama:
            type: string
            example: PT ABC
          lokasi:
            type: string
            example: Jakarta
          id:
            type: string
            example: JKT0001

    responses:
      201:
        description: Success add new peternakan to database
      400:
        description: missing Parameter
    """
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
        }, 404)

    responses = DBUtil().add_peternak(peternakModel)
    if responses != "ok":
        return make_response({
            'status': 'error',
            'message': responses,
        }, 404)

    return make_response({
        'status': 'ok',
    }, 201)
