import glob
import os
import utils
import base64
import json
import logging
import SqliteServices


class RainController:
    sqlite = None

    def __init__(self):
        self.sqlite = SqliteServices.SqliteService("/ops/data/rainDropLedger.db")
        print("Controller Initialized")

    def addVehicleData(self, dropId, requestBody):
        vdString = self.decodeBase64(requestBody)
        vehicleDataObj = self.stringToJsonObj(vdString)
        tableName = "vehicleData"
        #print(vehicleDataObj)

        vData =  ['"'+vehicleDataObj[0]['dropId']+'"', '"'+vehicleDataObj[1]['px4_autopilot_version']+'"', '"'+vehicleDataObj[2]['autopilot_ftp']+'"' ]
        vData += ['"'+vehicleDataObj[3]['globalLoc']+'"', '"'+vehicleDataObj[4]['globalLoc_relAlt']+'"', '"'+vehicleDataObj[5]['localLoc']+'"' ]
        vData += ['"'+vehicleDataObj[6]['attitude']+'"', '"'+vehicleDataObj[7]['velocity']+'"', '"'+vehicleDataObj[8]['gps']+'"', '"'+vehicleDataObj[9]['groundspeed']+'"' ]
        vData += ['"'+vehicleDataObj[10]['airspeed']+'"', '"'+vehicleDataObj[11]['gimbalStatus']+'"', '"'+vehicleDataObj[12]['battery']+'"' ]
        vData += ['"'+vehicleDataObj[13]['ekf_ok']+'"', '"'+vehicleDataObj[14]['last_heartbeat']+'"', '"'+vehicleDataObj[15]['rangefinder']+'"' ]
        vData += ['"'+vehicleDataObj[16]['rangefinder_distance']+'"', '"'+vehicleDataObj[17]['rangefinder_voltage']+'"', '"'+vehicleDataObj[18]['heading']+'"' ]
        vData += ['"'+vehicleDataObj[19]['isArmable']+'"', '"'+vehicleDataObj[20]['systemStatus']+'"', '"'+vehicleDataObj[21]['mode']+'"', '"'+vehicleDataObj[22]['armed']+'"' ]

        print(vData)

        insertStatus, insertMessage = self.sqlite.insertToTable(tableName, vData, 0, "dialogId")
        print("InsertRecordResult: {} {} {}".format(insertMessage, str(insertStatus), tableName))
        logging.info("InsertRecordResult: {} {} {}".format(insertMessage, str(insertStatus), tableName))
        return insertStatus

    def registerVehicle(self, dropId, registrationId, vType):
        vehicleParams = ['"' + dropId + '"', '"' + registrationId + '"', '"' + vType + '"']
        tableName = "registeredVehicles"
        insertStatus, insertMessage = self.sqlite.insertToTable(tableName, vehicleParams, 0, "dropId")
        print("InsertRecordResult: {} {} {}".format(insertMessage, str(insertStatus), tableName))
        logging.info("InsertRecordResult: {} {} {}".format(insertMessage, str(insertStatus), tableName))
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
            {"text": "gps"},
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