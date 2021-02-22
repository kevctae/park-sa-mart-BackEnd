from app import *

def addcar():
    email = request.json['email']
    platenum = request.json['platenum']
    cur = mysql.connection.cursor()
    checkValue = cur.execute('SELECT email FROM Cars WHERE platenum = %s', (platenum,))
    if checkValue > 0:
        carDetail = cur.fetchone()
        if carDetail['email'] == None:
            cur.execute('UPDATE Cars SET email = %s WHERE platenum = %s', (email,platenum,))
            mysql.connection.commit()
            cur.close()
            return jsonify({'message':'Done'})
        else:
            mysql.connection.commit()
            cur.close()
            return jsonify({'message':'Car Already Owned'})
    else:
        cur.execute('INSERT INTO Cars(platenum,email) VALUES(%s,%s)', (platenum,email,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message':'Done'})