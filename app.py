from flask import Flask, request, make_response

import routes.Login as loginRoute
import routes.Input as inputRoute

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


app.add_url_rule('/login', view_func=loginRoute.login)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
