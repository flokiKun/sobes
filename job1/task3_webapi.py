import flask
from flask import request
from task3 import appearance
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = False


@app.route('/api/get_duration', methods=['GET'])
def api_get_duration():
    data = request.get_json()
    data_dict = json.loads(data)
    resoponse = appearance(data_dict['data'])
    # print(resoponse)
    return str(resoponse)


if __name__ == '__main__':
    app.run()