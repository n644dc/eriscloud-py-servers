import glob
import os
import utils
import base64
import json
import SqliteServices


class RainController:
    sqlite = None

    def __init__(self):
        self.sqlite = SqliteServices.SqliteService("/ops/data/rainDropLedger.db")
        print("Controller Initialized")


    def addVehicleData(self, dropId, requestBody):
        vdString = self.decodeBase64(requestBody)
        vehicleDataObj = self.stringToJsonObj(vdString)
        print(vehicleDataObj["test"])


    def registerVehicle(self, dropId, registrationId, vType):
        vehicleParams = ['"' + dropId + '"', '"' + registrationId + '"', '"' + vType + '"']
        tableName = "registeredVehicles"
        insertStatus, insertMessage = self.sqlite.insertToTable(tableName, vehicleParams, 0, "dropId")
        print("InsertRecordResult: {} {} {}".format(insertMessage, str(insertStatus), tableName))
        return insertStatus


    def createCommDialog(self, dialogId, dropId, requestType, requestBody):
        commDialog = utils.CommRestDialog(dialogId, dropId, requestType, requestBody)
        return commDialog

    def saveCommDialog(self, commDialog):
        dialogParams = ['"'+commDialog.dialogId+'"', '"'+commDialog.dropId+'"', '"'+commDialog.requestType+'"', '"'+commDialog.requestBody+'"', '"'+commDialog.responseType+'"', '"'+commDialog.responseBody+'"']
        tableName = "restDialogs"
        insertStatus, insertMessage = self.sqlite.insertToTable(tableName, dialogParams, 0, "dialogId")
        print("InsertRecordResult: {} {} {}".format(insertMessage, str(insertStatus), tableName))


    def decodeBase64(self, base64text):
        base64_bytes = base64text.encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)
        dataString = message_bytes.decode('ascii')
        return dataString

    def stringToJsonObj(self, jsonString):
        dataObj = json.loads(jsonString)
        return dataObj


    def createRainDropDb(self):
        ###### Table restDialogs
        tableName = "restDialogs"
        columns = [
            {"text": "dialogId"},
            {"text": "dropId"},
            {"text": "requestType"},
            {"text": "requestBody"},
            {"text": "responseType"},
            {"text": "responseBody"}
        ]
        createStatus, createMessage = self.sqlite.createTable(tableName, columns)
        print("TableCreationResult: " + createMessage)

        ###### Table vehicleData
        tableName = "vehicleData"
        columns = [
            {"text": "dropId"},
            {"text": "px4_autopilot_version"},
            {"text": "autopilot_ftp"},
            {"text": "globalLoc"},
            {"text": "globalLoc_relAlt"},
            {"text": "localLoc"},
            {"text": "attitude"},
            {"text": "velocity"},
            {"text": "groundspeed"},
            {"text": "airspeed"},
            {"text": "gimbalStatus"},
            {"text": "battery"},
            {"text": "ekf_ok"},
            {"text": "last_heartbeat"},
            {"text": "rangefinder"},
            {"text": "rangefinder_distance"},
            {"text": "rangefinder_voltage"},
            {"text": "heading"},
            {"text": "isArmable"},
            {"text": "systemStatus"},
            {"text": "mode"},
            {"text": "armed"}
        ]
        createStatus, createMessage = self.sqlite.createTable(tableName, columns)
        print("TableCreationResult: " + createMessage)

        ###### Table registeredVehicles
        tableName = "registeredVehicles"
        columns = [
            {"text": "dropId"},
            {"text": "registrationId"},
            {"text": "type"}
        ]
        createStatus, createMessage = self.sqlite.createTable(tableName, columns)
        print("TableCreationResult: " + createMessage)
# End Class RainController