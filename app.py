from flask import Flask, request, make_response

import routes.Login as loginRoute
import routes.Input as inputRoute
import routes.GetBatch as getBatch

app = Flask(__name__)

app.add_url_rule('/login', view_func=loginRoute.login)
app.add_url_rule('/getBatch', view_func=getBatch.getBatch)
app.add_url_rule('/inputBatch', view_func=inputRoute.inputBatch())

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
