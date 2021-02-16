from flask import Flask
from flask import request
from flask import jsonify

server = Flask(__name__)

class commRestDialog:
    def __init__(self, reqId, reqType, reqBody, resBody=None):
        self.rainDropId   = reqId
        self.requestType  = reqType
        self.requestBody  = reqBody
        self.responseBody = resBody

    @property
    def serialize(self):
        return {
            'rainDropId': self.rainDropId,
            'requestType': self.requestType,
            'requestBody': self.requestBody,
            'responseBody': self.responseBody
        }



@server.route('/', methods=['GET'])
def hello():
    return "NO-OP"

@server.route('/raindrop/heartbeat', methods=['GET','POST'])
def rainDropHeartbeat():
    rainDropID  = request.args.get('rainDropId', '')
    requestType = request.args.get('requestType', '')
    requestBody = request.args.get('requestBody', '')

    commDialog = commRestDialog(rainDropID, requestType, requestBody)

    return jsonify(dialog=commDialog.serialize)

@server.route('/raindrop/sequence/<sequence>')
def rainDropOmnibus(sequence):
    return "Hello {}!".format(sequence)

if __name__ == '__main__':
    server.run(host='0.0.0.0', port=1068)