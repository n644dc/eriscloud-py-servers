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