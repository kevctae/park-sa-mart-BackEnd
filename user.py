from app import *

def editprofile():
    old_email = request.json['old_email']
    email = request.json['email']
    password = request.json['password']
    fname = request.json['fname']
    lname = request.json['lname']
    cur = mysql.connection.cursor()
    checkValue = cur.execute('SELECT email FROM Account WHERE email = %s', (email,))
    if checkValue > 0:
        mysql.connection.commit()
        cur.close()
        return jsonify({'message' : 'EMAIL_EXISTED'})
    else:
        cur.execute('UPDATE Account SET email = %s, password = %s, fname = %s, lname = %s WHERE email = %s', (email,password,fname,lname,old_email,))
        expiredate = datetime.datetime.utcnow() + datetime.timedelta(seconds=120)
        token = jwt.encode({'email': email, 'exp' : expiredate}, app.config['SECRET_KEY'])
        mysql.connection.commit()
        cur.close()
        return jsonify({'email' : email, 'token' : token, 'expiresIn' : '120'})


def addcar():
    email = request.json['email']
    platenum = request.json['platenum']
    platecity = request.json['platecity']
    expiredate = datetime.datetime.utcnow() + datetime.timedelta(seconds=120)
    token = jwt.encode({'email': email, 'exp' : expiredate}, app.config['SECRET_KEY'])
    cur = mysql.connection.cursor()
    checkValue = cur.execute('SELECT email FROM Cars WHERE platenum = %s and platecity = %s', (platenum,platecity,))
    if checkValue > 0:
        mysql.connection.commit()
        cur.close()
        return jsonify({'message':'CAR_OWNED'})
    else:
        cur.execute('INSERT INTO Cars(platenum,platecity,email) VALUES(%s,%s,%s)', (platenum,platecity,email,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'email' : email, 'token' : token, 'expiresIn' : '120'})

def removecar():
    email = request.json['email']
    platenum = request.json['platenum']
    platecity = request.json['platecity']
    expiredate = datetime.datetime.utcnow() + datetime.timedelta(seconds=120)
    token = jwt.encode({'email': email, 'exp' : expiredate}, app.config['SECRET_KEY'])
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM Cars WHERE email = %s and platenum = %s and platecity = %s', (email,platenum,platecity,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'email' : email, 'platenum' : platenum, 'platecity' : platecity, 'token' : token, 'expiresIn' : '120'})


def addcard():
    email = request.json['email']
    card_no = request.json['card_no']
    exp_year = request.json['exp_year']
    exp_month = request.json['exp_month']
    cvv = request.json['cvv']
    fname = request.json['fname']
    lname = request.json['lname']
    expiredate = datetime.datetime.utcnow() + datetime.timedelta(seconds=120)
    token = jwt.encode({'email': email, 'exp' : expiredate}, app.config['SECRET_KEY'])
    cur = mysql.connection.cursor()
    checkValue = cur.execute('SELECT * FROM Card WHERE card_no = %s', (card_no,))
    cur.fetchall()
    if checkValue == 0:
        cur.execute('INSERT INTO Card(card_no,exp_year,exp_month,cvv,fname,lname) VALUES(%s,%s,%s,%s,%s,%s)', (card_no, exp_year, exp_month, cvv, fname, lname,))
    cur.fetchall()
    checkValue = cur.execute('SELECT * FROM CardOwns WHERE card_no = %s and email = %s', (card_no,email,))
    if checkValue > 0:
        mysql.connection.commit()
        cur.close()
        return jsonify({'message' : 'USER_ALREADY_OWNS_CARD'})
    else:
        cur.execute('INSERT INTO CardOwns(card_no,email) VALUES(%s,%s)', (card_no, email,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'email' : email, 'card_no' : card_no, 'token' : token, 'expiresIn' : '120'})

def removecard():
    email = request.json['email']
    card_no = request.json['card_no']
    expiredate = datetime.datetime.utcnow() + datetime.timedelta(seconds=120)
    token = jwt.encode({'email': email, 'exp' : expiredate}, app.config['SECRET_KEY'])
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM CardOwns WHERE email = %s and card_no = %s', (email,card_no,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'email' : email, 'card_no' : card_no, 'token' : token, 'expiresIn' : '120'})