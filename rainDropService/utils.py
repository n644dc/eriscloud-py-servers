import glob
import os


class CommRestDialog:
    def __init__(self, dialogId, dropId, reqType, reqBody, resType=None, resBody=None):
        self.dialogId     = dialogId
        self.dropId       = dropId
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
            'dialogId':     self.dialogId,
            'rainDropId':   self.dropId,
            'requestType':  self.requestType,
            'requestBody':  self.requestBody,
            'responseType': self.responseType,
            'responseBody': self.responseBody
        }

    @property
    def toString(self):
        return str(self.serialize)

class GlobalParams:
    
    REQUEST_TYPES = []
    RESPONSE_TYPES = []

    def __init__(self):
        pass

    