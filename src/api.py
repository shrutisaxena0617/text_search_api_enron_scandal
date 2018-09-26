import json

from flask import Flask, request, Response

from src.solution import TokenMap

app = Flask(__name__)


@app.route('/search', methods=['GET'])
def apicall():
    keys = request.args.getlist('key')
    responseDict = {}
    for key in keys:
        responseDict[key] = obj.master_dict.get(key, [])
    js = json.dumps(responseDict, default=lambda x: x.__dict__, ensure_ascii=False)
    resp = Response(js, status=200, mimetype='application/json')
    return resp


if __name__ == '__main__':
    obj = TokenMap()
    obj.parseText()
    app.run(debug=True, port=5000)  # run app in debug mode on port 5000
