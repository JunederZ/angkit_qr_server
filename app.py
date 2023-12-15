from flask import Flask, request
from flasgger import Swagger, LazyString, LazyJSONEncoder
import routes

app = Flask(__name__)
app.json_encoder = LazyJSONEncoder

swagger = Swagger(app)

app.add_url_rule('/login', view_func=routes.login)
app.add_url_rule('/getBatch', view_func=routes.getBatch)
app.add_url_rule('/inputBatch', view_func=routes.inputBatch)
app.add_url_rule('/addPeternakan', view_func=routes.addPeternakan, methods=['POST'])
app.add_url_rule('/addDistributor', view_func=routes.addDistributor, methods=['POST'])

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
