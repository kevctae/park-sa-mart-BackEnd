from app import *



def register():
    if request.method == 'GET':
        return 'test get'
    else:
        email = request.json['email']
        password = request.json['password']
        fname = request.json['fname']
        lname = request.json['lname']
        cur = mysql.connection.cursor()
        checkValue = cur.execute('SELECT * FROM Account WHERE email = %s', (email,))
        if checkValue > 0:
            mysql.connection.commit()
            cur.close()
            return jsonify({'message' : 'EMAIL_EXISTED'})
        else:
            cur.execute('INSERT INTO Account(email,password,fname,lname) VALUES(%s,%s,%s,%s)', (email,password,fname,lname,))
            expiredate = '120'
            token = jwt.encode({'email': email, 'exp' : expiredate}, app.config['SECRET_KEY'])
            mysql.connection.commit()
            cur.close()
            return jsonify({'token' : token, 'email' : email, 'expiresIn' : expiredate})

def login():
    email = request.json['email']
    password = request.json['password']
    cur = mysql.connection.cursor()
    checkValue = cur.execute('SELECT email,password FROM Account WHERE email = %s AND password = %s', (email,password,))
    if checkValue != 0:
        userAcc = cur.fetchone()
        expiredate = '120'
        token = jwt.encode({'email': userAcc['email'], 'exp' : expiredate}, app.config['SECRET_KEY'])
        mysql.connection.commit()
        cur.close()
        return jsonify({'email': userAcc['email'], 'token' : token, 'expiresIn' : expiredate})
    else:
        mysql.connection.commit()
        cur.close()
        return jsonify({'message' : 'INVALID_EMAIL_OR_PASSWORD'})