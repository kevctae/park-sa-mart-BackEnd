from app import *

def addcar():
    email = request.json['email']
    platenum = request.json['platenum']
    city = request.json['city']
    cur = mysql.connection.cursor()
    checkValue = cur.execute('SELECT email FROM Cars WHERE platenum = %s AND city = %s', (platenum,city,))
    if checkValue > 0:
        carDetail = cur.fetchone()
        if carDetail['email'] == None:
            cur.execute('UPDATE Cars SET email = %s WHERE platenum = %s AND city = %s', (email,platenum,city,))
            mysql.connection.commit()
            cur.close()
            return jsonify({'message':'Done'})
        else:
            mysql.connection.commit()
            cur.close()
            return jsonify({'message':'Car Already Owned'})
    else:
        cur.execute('INSERT INTO Cars(platenum,city,email) VALUES(%s,%s,%s)', (platenum,city,email,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message':'Done'})