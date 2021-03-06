from flask import Flask, request, jsonify, session, url_for, redirect, flash
from flask_mysqldb import MySQL
import yaml
import pymysql
from functools import wraps
import jwt
import datetime
from flask_cors import CORS
import math
import pytz


app = Flask(__name__)
cors = CORS(app)

db = yaml.load(open('db.yaml'), Loader=yaml.FullLoader)
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_PORT'] = db['mysql_port']
app.config['JSON_SORT_KEYS'] = False
app.config['SECRET_KEY'] = 'parksamart'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
tz = pytz.timezone('Asia/Bangkok')
mysql = MySQL(app)

def generate_token(email):
    expiredate = datetime.datetime.utcnow() + datetime.timedelta(seconds=7200)
    token = jwt.encode({'email': email, 'exp' : expiredate}, app.config['SECRET_KEY'])
    return token

import user
import auth
import camera
import parking
import payment

# def check_token(func):
#     @wraps(func)
#     def wrapped(*args, **kwargs):
#         token = request.args.get('token')
#         if not token:
#             return jsonify({'message' : 'Missing token'}), 403
#         try:
#             data = jwt.decode(token, app.config['SECRET_KEY'], 'HS256')
#         except:
#             return jsonify({'message' : 'Invalid token'}), 403
#         return func(*args, **kwargs)
#     return wrapped

def check_token(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        try:
            token = request.json['token']
            try:
                data = jwt.decode(token, app.config['SECRET_KEY'], 'HS256')
            except:
                return jsonify({'message' : 'INVALID_TOKEN'}), 403
        except:
            return jsonify({'message' : 'MISSING_TOKEN'}), 403
        
        return func(*args, **kwargs)
    return wrapped



@app.route('/register', methods=['POST'])
def register():
    return auth.register()

@app.route('/login', methods=['POST'])
def login():
    return auth.login()

@app.route('/home', methods=['GET', 'POST'])
@check_token
def home():
    token = request.json['token']
    email = jwt.decode(token, app.config['SECRET_KEY'], 'HS256')['email']
    return email + ' you have valid token'


@app.route('/addcar', methods=['POST'])
@check_token
def addcar():
    return user.addcar()

@app.route('/removecar', methods=['POST'])
@check_token
def removecar():
    return user.removecar()


@app.route('/editprofile', methods=['POST'])
@check_token
def editprofile():
    return user.editprofile()

@app.route('/addcard', methods=['POST'])
@check_token
def addcard():
    return user.addcard()

@app.route('/removecard', methods=['POST'])
@check_token
def removecard():
    return user.removecard()

@app.route('/setprimarycard', methods=['POST'])
@check_token
def setprimarycard():
    return user.setprimarycard()

@app.route('/returncarlist', methods=['POST'])
@check_token
def returncarlist():
    return user.returncarlist()

@app.route('/setmainpaymentmethod', methods=['POST'])
@check_token
def setmainpaymentmethod():
    return user.setmainpaymentmethod()

@app.route('/retrieveprofile', methods=['POST'])
@check_token
def retrieveprofile():
    return user.retrieveprofile()

@app.route('/carentry', methods=['POST'])
def carentry():
    return camera.carentry()

@app.route('/updatecarfloor', methods=['POST'])
def updatecarfloor():
    return camera.updatecarfloor()

@app.route('/topupwallet', methods=['POST'])
@check_token
def topupwallet():
    return user.topupwallet()

@app.route('/currentparkingsession', methods=['POST'])
@check_token
def currentparkingsession():
    return parking.currentparkingsession()

@app.route('/getavailableparkingspace', methods=['GET'])
def getavailableparkingspace():
    return parking.getavailableparkingspace()

@app.route('/carexit', methods=['POST'])
def carexit():
    return camera.carexit()

@app.route('/memberpaynow', methods=['POST'])
@check_token
def memberpaynow():
    return payment.memberpaynow()

@app.route('/recentparkingsessions', methods=['POST'])
@check_token
def recentparkingsessions():
    return user.recentparkingsessions()


if __name__ == '__main__' :     
    app.run(debug=True, host = '0.0.0.0')
