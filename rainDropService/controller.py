import glob
import os
import utils
import SqliteServices


class RainDropController:
    sqlite = None

    def __init__(self):
        self.sqlite = SqliteServices.SqliteService("/ops/data/rainDropLedger.db")
        print("Controller Initialized")

    def createCommDialog(self, dialogId, dropId, requestType, requestBody):
        commDialog = utils.commRestDialog(dialogId, dropId, requestType, requestBody)
        print(commDialog.toString())
        
        return commDialog

    def saveCommDialog(self, commDialog):

        insertStatus, insertMessage = self.sqlite.insertToTable("restDialogs", ['"'+commDialog.dialogId+'"', '"'+commDialog.dropId+'"', '"'+commDialog.requestType+'"', '"'+commDialog.requestBody+'"', '"'+commDialog.responseType+'"', '"'+commDialog.responseBody+'"'], "dialogId")
        print("\nInsertRecordResult: {} {}".format(insertMessage, str(insertStatus)))

    def createRainDropDb(self):
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
        print("\nTableCreationResult: " + createMessage)

        resultsArray, selectMessage = self.sqlite.selectFromTable(tableName)
        print(str(resultsArray))