from app import *

def addcar():
    email = request.json['email']
    platenum = request.json['platenum']
    platecity = request.json['platecity']
    cur = mysql.connection.cursor()
    checkValue = cur.execute('SELECT email FROM Cars WHERE platenum = %s and platecity = %s', (platenum,platecity,))
    if checkValue > 0:
        mysql.connection.commit()
        cur.close()
        return jsonify({'message':'Car Already Owned'})
    else:
        cur.execute('INSERT INTO Cars(platenum,platecity,email) VALUES(%s,%s,%s)', (platenum,platecity,email,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message':'Done'})


def editprofile():
    old_email = request.json['old_email']
    email = request.json['email']
    password = request.json['password']
    fname = request.json['fname']
    lname = request.json['lname']
    cur = mysql.connection.cursor()
    checkValue = cur.execute('SELECT email FROM Account WHERE email = %s', (email,))
    if checkValue > 0:
        return jsonify({'message' : 'EMAIL_EXISTED'})
    else:
        cur.execute('UPDATE Account SET email = %s, password = %s, fname = %s, lname = %s WHERE email = %s', (email,password,fname,lname,old_email,))
        expiredate = datetime.datetime.utcnow() + datetime.timedelta(seconds=120)
        token = jwt.encode({'email': userAcc['email'], 'exp' : expiredate}, app.config['SECRET_KEY'])
        mysql.connection.commit()
        cur.close()
        return jsonify({'email' : email, 'token' : token})