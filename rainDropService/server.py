import sys
import controller
import uuid
from logging.config import dictConfig
from flask import Flask
from flask import request
from flask import jsonify

server = Flask(__name__)
control = controller.RainDropController()

@server.route('/raindrop/params/global', methods=['POST'])
def getGlobalParams(self):
    return ""


@server.route('/raindrop/sequence', methods=['GET', 'POST'])
def rainDropBus():
    restDialogId = str(uuid.uuid4())
    commDialog = controller.createCommDialog(restDialogId, request.json["rainDropId"], request.json["requestType"], request.json["requestBody"])
    
    responseType = "REGISTRATION_RESPONSE"
    responseBody = "Rain drop registered successfully."
    commDialog.setResponse([responseType, responseBody])
    
    print(commDialog.toString, file=sys.stderr)
    return jsonify(dialog=commDialog.serialize)




if __name__ == '__main__':
    #Args: port, isDebug
    server.run(host='0.0.0.0', port=1068, debug=True)