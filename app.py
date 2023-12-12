from flask import Flask, request, make_response

import routes.Login as loginRoute
import routes.InputBatch as inputRoute
import routes.GetBatch as getBatch
import routes.AddPeternakan as addPeternakan
import routes.AddDistributor as addDistributor

app = Flask(__name__)

app.add_url_rule('/login', view_func=loginRoute.login)
app.add_url_rule('/getBatch', view_func=getBatch.getBatch)
app.add_url_rule('/inputBatch', view_func=inputRoute.inputBatch)
app.add_url_rule('/addPeternakan', view_func=addPeternakan.addPeternakan)
app.add_url_rule('/addDistributor', view_func=addDistributor.addDistributor)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
