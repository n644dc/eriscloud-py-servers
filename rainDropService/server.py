import sys
from logging.config import dictConfig
from flask import Flask
from flask import request
from flask import jsonify

server = Flask(__name__)

class commRestDialog:
    def __init__(self, dropId, reqType, reqBody, resType=None, resBody=None):
        self.rainDropId   = dropId
        self.requestType  = reqType
        self.requestBody  = reqBody

        self.responseType = resType
        self.responseBody = resBody

    def setResponse(self, response):
        self.responseType = response[0]
        self.responseBody = response[1]

    @property
    def serialize(self):
        return {
            'rainDropId': self.rainDropId,
            'requestType': self.requestType,
            'requestBody': self.requestBody,
            'responseType': self.responseType,
            'responseBody': self.responseBody
        }

    @property
    def toString(self):
        return str(self.serialize)

#class clientHandler:
#    def __init__(self):
#        continue

@server.route('/raindrop/params/global', methods=['POST'])
def getGlobalParams(self):
    return ""


@server.route('/raindrop/sequence', methods=['POST'])
def rainDropBus():
    commDialog = commRestDialog(request.json["rainDropId"], request.json["requestType"], request.json["requestBody"])
    
    responseType = "REGISTRATION_RESPONSE"
    responseBody = "Rain drop registered successfully."
    commDialog.setResponse([responseType, responseBody])
    
    print(commDialog.toString, file=sys.stderr)
    return jsonify(dialog=commDialog.serialize)




if __name__ == '__main__':
    #Args: port, isDebug
    server.run(host='0.0.0.0', port=1068, debug=True)