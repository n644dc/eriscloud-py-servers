import sys
import uuid
import base64
from logging.config import dictConfig
from flask import Flask
from flask import request
from flask import jsonify
from flask import redirect, render_template
from flask_cors import CORS, cross_origin

server = Flask(__name__)

def decodeBase64(base64text):
    base64_bytes = base64text.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    dataString = message_bytes.decode('ascii')
    return dataString

def encodeBase64(plainText):
    linkBytes = plainText.encode("ascii")
    base64Bytes = base64.b64encode(linkBytes) 
    jsonStringBase64 = base64Bytes.decode("ascii")
    return jsonStringBase64

####################################
@server.route('/')
def home():
    return render_template('index.html')

####################################
@server.route('/seturl')
def setUrl():
    print("HIT first on setURL")
    link64 = encodeBase64(request.args.get('link'))
    print("about to return")
    return "http://eriscloud.one:88/x/" + link64

####################################
@server.route('/x/<linkBase64>', methods=['POST'])
def redirectToLink(linkBase64):
    stringUrl = decodeBase64(linkBase64)
    return redirect(stringUrl, code=302)


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=88, debug=True)
