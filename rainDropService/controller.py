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
        print("TableCreationResult: " + createMessage)

        insertStatus, insertMessage = self.sqlite.insertToTable(tableName, ["\"123123-332123-32323-232\"", "\"rd01\"", "\"REGISTER\"", "\"request body here\"", "\"REG_SUCCESS\"", "\"Registration was successful\""])
        print("InsertRecordResult: " + insertMessage)

        resultsArray, selectMessage = self.sqlite.selectFromTable(tableName)
        print(str(resultsArray))