from app import *

def carentry():
    try:
        entry_picture = request.json['entry_picture']
        building = request.json['building']
        floor = request.json['floor']
        parking_platenum = request.json['parking_platenum']
        parking_platecity = request.json['parking_platecity']
        entry_date = request.json['entry_date']
        entry_time = request.json['entry_time']
    except:
        return jsonify({'message' : 'Failed'})
    cur = mysql.connection.cursor()
    checkValue = cur.execute('SELECT email FROM Cars WHERE platenum = %s and platecity = %s', (parking_platenum,parking_platecity,))
    if checkValue > 0:
        result = cur.fetchone()
        email = result['email']
    else:
        cur.fetchall()
        email = None
    cur.execute('INSERT INTO Parking_record(entry_picture,building,floor,parking_platenum,parking_platecity,entry_date,entry_time,email) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)', (entry_picture,building,floor,parking_platenum,parking_platecity,entry_date,entry_time,email,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message' : 'Success'})
    