from flask import Flask, request, make_response
from database.db_util import DBUtil

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/login')
def login():

    # data = request.get_data()
    # data_bytes = base64.b64decode(data)
    # decrypted_json = json.loads(cryptUtil.decode(data_bytes))

    json = request.get_json()
    username = json.get('username')
    password = json.get('password')

    user = DBUtil().user_login(username, password)
    if user == 'success':
        return make_response({
            'status': user,
        }, 200)
    return make_response({
        'status': user,
    }, 200)


if __name__ == '__main__':
    app.run()
