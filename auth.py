from app import *



def register():
    if request.method == 'GET':
        return 'test get'
    else:
        try:
            email = request.json['email']
            password = request.json['password']
            fname = request.json['fname']
            lname = request.json['lname']
        except:
            return jsonify({'message' : 'BAD_PAYLOAD'}) ,400
        cur = mysql.connection.cursor()
        checkValue = cur.execute('SELECT * FROM Account WHERE email = %s', (email,))
        if checkValue > 0:
            mysql.connection.commit()
            cur.close()
            return jsonify({'message' : 'EMAIL_EXISTED'}) ,409
        else:
            cur.execute('INSERT INTO Account(email,password,fname,lname) VALUES(%s,%s,%s,%s)', (email,password,fname,lname,))
            token = generate_token(email)
            mysql.connection.commit()
            cur.close()
            return jsonify({'token' : token, 'email' : email, 'expiresIn' : '600'}) ,201

def login():
    try:
        email = request.json['email']
        password = request.json['password']
    except:
        return jsonify({'message' : 'BAD_PAYLOAD'}) , 400
    cur = mysql.connection.cursor()
    checkValue = cur.execute('SELECT email,password FROM Account WHERE email = %s AND password = %s', (email,password,))
    if checkValue != 0:
        userAcc = cur.fetchone()
        token = generate_token(email)
        mysql.connection.commit()
        cur.close()
        return jsonify({'email': userAcc['email'], 'token' : token, 'expiresIn' : '600'}), 200
    else:
        mysql.connection.commit()
        cur.close()
        return jsonify({'message' : 'INVALID_EMAIL_OR_PASSWORD'}), 403