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