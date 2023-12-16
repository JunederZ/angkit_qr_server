from flask import Flask, request
from flasgger import Swagger, LazyString, LazyJSONEncoder
import routes

app = Flask(__name__)
app.config['SWAGGER'] = {
    'title': 'API Angkit Agro QR',
    'description': 'API documentation for Angkit Agro QR'
}
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
app.add_url_rule('/checkUser', view_func=routes.checkUser, methods=['POST'] )
app.add_url_rule('/login', view_func=routes.login)
app.add_url_rule('/getBatch', view_func=routes.getBatch, methods=['POST'])
app.add_url_rule('/inputBatch', view_func=routes.inputBatch, methods=['POST'])
app.add_url_rule('/addPeternakan', view_func=routes.addPeternakan, methods=['POST'])
app.add_url_rule('/addDistributor', view_func=routes.addDistributor, methods=['POST'])

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, host="0.0.0.0", port=5001)
