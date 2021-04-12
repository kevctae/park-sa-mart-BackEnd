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
        token = generate_token(email)
        mysql.connection.commit()
        cur.close()
        return jsonify({'email' : email, 'token' : token, 'expiresIn' : '600'})


def addcar():
    email = request.json['email']
    platenum = request.json['platenum']
    platecity = request.json['platecity']
    brand = request.json['brand']
    model = request.json['model']
    token = generate_token(email)
    cur = mysql.connection.cursor()
    checkValue = cur.execute('SELECT email FROM Cars WHERE platenum = %s and platecity = %s', (platenum,platecity,))
    if checkValue > 0:
        mysql.connection.commit()
        cur.close()
        return jsonify({'message':'CAR_OWNED'})
    else:
        cur.execute('INSERT INTO Cars(platenum,platecity,email,brand,model) VALUES(%s,%s,%s,%s,%s)', (platenum,platecity,email,brand,model,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'email' : email, 'token' : token, 'expiresIn' : '600'})

def removecar():
    email = request.json['email']
    platenum = request.json['platenum']
    platecity = request.json['platecity']
    token = generate_token(email)
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM Cars WHERE email = %s and platenum = %s and platecity = %s', (email,platenum,platecity,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'email' : email, 'platenum' : platenum, 'platecity' : platecity, 'token' : token, 'expiresIn' : '600'})


def addcard():
    email = request.json['email']
    card_no = request.json['card_no']
    exp_year = request.json['exp_year']
    exp_month = request.json['exp_month']
    cvv = request.json['cvv']
    fname = request.json['fname']
    lname = request.json['lname']
    token = generate_token(email)
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
        return jsonify({'email' : email, 'card_no' : card_no, 'token' : token, 'expiresIn' : '600'})

def removecard():
    email = request.json['email']
    card_no = request.json['card_no']
    token = generate_token(email)
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM CardOwns WHERE email = %s and card_no = %s', (email,card_no,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'email' : email, 'card_no' : card_no, 'token' : token, 'expiresIn' : '600'})

def setprimarycard():
    email = request.json['email']
    card_no = request.json['card_no']
    token = generate_token(email)
    cur = mysql.connection.cursor()
    checkValue = cur.execute('SELECT * FROM CardOwns WHERE email = %s and card_no = %s', (email,card_no,))
    if checkValue > 0:
        cur.fetchall()
        cur.execute('UPDATE Account SET primary_card_no = %s WHERE email = %s', (card_no,email,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'email' : email, 'card_no' : card_no, 'token' : token, 'expiresIn' : '600'})
    else:
        mysql.connection.commit()
        cur.close()
        return jsonify({'message' : 'CARD_NOT_OWNED_BY_THE_USER'})


def returncarlist():
    email =  request.json['email']
    cur= mysql.connection.cursor()
    checkValue = cur.execute('SELECT platenum,platecity,brand,model FROM Cars WHERE email = %s ', (email,))
    if checkValue > 0:
        myresult = cur.fetchall()
        cur.close()
        return jsonify(myresult)
    else:
        mysql.connection.commit()
        cur.close()
        return jsonify({'message' : 'NO_CAR_OWNED'})

def setmainpaymentmethod():
    email = request.json['email']
    method = request.json['method']
    token = generate_token(email)
    cur = mysql.connection.cursor()
    if method == 'Wallet':
        cur.execute('UPDATE Account SET main_payment_method = %s WHERE email = %s', (method,email,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'email' : email, 'method' : method, 'token' : token, 'expiresIn' : '600'})
    elif method == 'VISA':
        card_no = request.json['card_no']
        checkValue = cur.execute('SELECT * FROM CardOwns WHERE email = %s and card_no = %s', (email,card_no,))
        if checkValue == 0:
            mysql.connection.commit()
            cur.close()
            return jsonify({'message' : 'CARD_NOT_OWNED_BY_THE_USER'})
        cur.fetchall()
        cur.execute('UPDATE Account SET main_payment_method = %s, primary_card_no = %s WHERE email = %s', (method,card_no,email,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'email' : email, 'method' : method, 'token' : token, 'expiresIn' : '600'})
    else:
        mysql.connection.commit()
        cur.close()
        return jsonify({'message' : 'METHOD_CAN_ONLY_BE_CARD_OR_WALLET'})

def retrieveprofile():
    email= request.json['email']
    token = generate_token(email)
    cur=mysql.connection.cursor()
    checkvalue = cur.execute('SELECT fname,lname,wallet,main_payment_method,primary_card_no FROM Account WHERE email = %s' , (email,))
    if checkvalue>0:
        result=cur.fetchone()
        cur.close()
        result['token'] = token
        result['expiresIn'] = '600'
        return jsonify(result)
    else:
        mysql.connection.commit()
        cur.close()
        return jsonify({'message' : 'INVALID_EMAIL'})

def topupwallet():
    email = request.json['email']
    money_to_add = request.json['money_to_add']
    cur = mysql.connection.cursor()
    checkValue = cur.execute('SELECT * FROM Account WHERE email = %s', (email,))
    token = generate_token(email)
    if checkValue > 0:
        result = cur.fetchone()
        try:
            wallet = result['wallet'] + money_to_add
        except:
            mysql.connection.commit()
            cur.close()
            return jsonify({'message' : 'MONEY_SHOULD_ONLY_CONTAIN_NUMBER'})
        cur.execute('UPDATE Account SET wallet = %s WHERE email = %s', (wallet,email,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'email' : email, 'wallet' : wallet, 'token' : token, 'expiresIn' : '600'})
    else:
        mysql.connection.commit()
        cur.close()
        return jsonify({'message' : 'INVALID_EMAIL'})
     