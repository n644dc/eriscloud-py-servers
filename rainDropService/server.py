import sys
import uuid
import base64
import controller
from logging.config import dictConfig
from flask import Flask
from flask import request
from flask import jsonify

server = Flask(__name__)

####################################
@server.route('/portal/getTableData', methods=['GET', 'POST'])
def getTableData():
    control = controller.RainController()
    control.createRainDropDb()

    resultsArray, status = control.sqlite.selectFromTable(request.args.get('tablename'))
    control.sqlite.closeConnection()
    if status == "OK":
        return jsonify(resultsArray)
    return ""

####################################
@server.route('/raindrop/sequence', methods=['POST'])
def rainDropBus():
    responseType = "ACK"
    responseBody = "NONE"
    control = controller.RainController()
    control.createRainDropDb()

    restDialogId = str(uuid.uuid4())

    commDialog = control.createCommDialog(restDialogId, request.json["rainDropId"], request.json["requestType"], request.json["requestBody"])


    if commDialog.requestType == "register":
        regSuccess = control.registerVehicle(commDialog.dropId, commDialog.dialogId, "rainDrop")
        if regSuccess:
            responseBody = "Successful Registration"
        else:
            responseBody = "ERROR: Already registered"
    if commDialog.requestType == "sendVehicleData":
        control.addVehicleData(commDialog.dropId, commDialog.requestBody)

    commDialog.setResponse([responseType, responseBody])
    control.saveCommDialog(commDialog)
    control.sqlite.closeConnection()
    return jsonify(dialog=commDialog.serialize)


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=1068, debug=True)
