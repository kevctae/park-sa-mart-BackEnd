from flask import Flask, request, jsonify, session, url_for, redirect, flash
from flask_mysqldb import MySQL
import yaml
import pymysql
from functools import wraps
import jwt
import datetime



app = Flask(__name__)
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['JSON_SORT_KEYS'] = False
app.config['SECRET_KEY'] = 'parksamart'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

import user
import auth

def check_token(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message' : 'Missing token'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], 'HS256')
        except:
            return jsonify({'message' : 'Invalid token'}), 403
        return func(*args, **kwargs)
    return wrapped

@app.route('/register', methods=['GET', 'POST'])
def register():
    return auth.register()

@app.route('/login', methods=['GET'])
def login():
    return auth.login()

@app.route('/home', methods=['GET', 'POST'])
@check_token
def home():
    token = request.args.get('token')
    email = jwt.decode(token, app.config['SECRET_KEY'], 'HS256')['email']
    return email + 'you have valid token'


@app.route('/addcar', methods=['POST'])
@check_token
def addcar():
    return user.addcar()

@app.route('/visitorentry', methods=['GET'])
def visitorentry():
    return parkman.visitorentry()



if __name__ == '__main__' :
    app.run(debug=True)

