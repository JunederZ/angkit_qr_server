from flask import Flask, request
from flasgger import Swagger, LazyString, LazyJSONEncoder
import routes
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SWAGGER'] = {
    'title': 'API Angkit Agro QR',
    'description': 'API documentation for Angkit Agro QR'
}
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLER')
swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'ApiDocs',
            "route": '/ApiDocs.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    # "static_folder": "static",  # must be set by user
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

swagger = Swagger(app, config=swagger_config)
app.add_url_rule('/checkUser', view_func=routes.check_user, methods=['GET'])
app.add_url_rule('/register', view_func=routes.register, methods=['POST'])
app.add_url_rule('/removeUser', view_func=routes.remove_user, methods=['DELETE'])
app.add_url_rule('/login', view_func=routes.login, methods=['POST'])
app.add_url_rule('/getBatch', view_func=routes.getBatch, methods=['GET'])
app.add_url_rule('/inputBatch', view_func=routes.inputBatch, methods=['POST'])
app.add_url_rule('/updateBatch', view_func=routes.update_batch, methods=['PUT'])
app.add_url_rule('/updateUser', view_func=routes.update_user, methods=['PUT'])
app.add_url_rule('/addPeternakan', view_func=routes.add_peternakan, methods=['POST'])
app.add_url_rule('/addDistributor', view_func=routes.add_distributor, methods=['POST'])
app.add_url_rule('/get_all_batches', view_func=routes.get_all_batch, methods=['GET'])
app.add_url_rule('/get_batches_by_farm', view_func=routes.get_batch_by_farm, methods=['POST'])
app.add_url_rule('/get_batches_by_dist', view_func=routes.get_batch_by_distributor, methods=['POST'])
app.add_url_rule('/add_batch_img', view_func=routes.add_image, methods=['POST'])

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, host="0.0.0.0", port=5001)
