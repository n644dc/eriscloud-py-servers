import sys
import uuid
import base64
import controller
from logging.config import dictConfig
from flask import Flask
from flask import request
from flask import jsonify

server = Flask(__name__)

@server.route('/raindrop/params/global', methods=['GET', 'POST'])
def getGlobalParams(self):
    return ""


@server.route('/raindrop/sequence', methods=['POST'])
def rainDropBus():
    control = controller.RainDropController()
    control.createRainDropDb()

    restDialogId = str(uuid.uuid4())

    commDialog = control.createCommDialog(restDialogId, request.json["rainDropId"], request.json["requestType"], request.json["requestBody"])

    responseType = "ACK"
    responseBody = "Received"
    commDialog.setResponse([responseType, responseBody])

    control.saveCommDialog(commDialog)


    base64Body     = commDialog.requestBody.encode("ascii") 
    byteStringBody = base64.b64decode(base64Body) 
    sample_string  = byteStringBody.decode("ascii") 
    print(sample_string)

    # Determine what to do with message.

    control.sqlite.closeConnection()
    print(commDialog.toString, file=sys.stderr)
    return jsonify(dialog=commDialog.serialize)


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=1068, debug=True)