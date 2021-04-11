from app import *

def carentry():
    try:
        entry_picture = request.json['entry_picture']
        building = request.json['building']
        floor = request.json['floor']
        parking_platenum = request.json['parking_platenum']
        parking_platecity = request.json['parking_platecity']
        entry_datetime = request.json['entry_datetime']
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
    try:
        cur.execute('INSERT INTO Parking_record(entry_picture,building,floor,parking_platenum,parking_platecity,entry_datetime,email) VALUES (%s,%s,%s,%s,%s,%s,%s)', (entry_picture,building,floor,parking_platenum,parking_platecity,entry_datetime,email,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message' : 'Success'})
    except:
        return jsonify({'message' : 'Failed'})
    
def updatecarfloor(): 
    try:
        building = request.json['building']
        floor = request.json['floor']
        parking_platenum = request.json['parking_platenum']
        parking_platecity = request.json['parking_platecity']
        update_datetime = request.json['update_datetime']
    except:
        return jsonify({'message' : 'Failed'})
    cur = mysql.connection.cursor()
    checkValue = cur.execute('SELECT * FROM Parking_record WHERE parking_platenum = %s and parking_platecity = %s and parking_id not in (select parking_id from Invoice)', (parking_platenum,parking_platecity,))
    if checkValue == 0:
        mysql.connection.commit()
        cur.close()
        return jsonify({'message' : 'Success'})
    result = cur.fetchone()
    entry_datetime = result['entry_datetime']
    update_datetime = datetime.datetime.strptime(update_datetime, '%Y-%m-%d %H:%M:%S')
    time_delta = (update_datetime - entry_datetime)
    total_seconds = time_delta.total_seconds()
    minutes = total_seconds/60
    if minutes < 15:
        cur.execute('UPDATE Parking_record SET building = %s, floor = %s WHERE parking_platenum = %s and parking_platecity = %s and parking_id not in (select parking_id from Invoice)', (building,floor,parking_platenum,parking_platecity,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message' : 'Success, Updated'})
    mysql.connection.commit()
    cur.close()
    return jsonify({'message' : 'Success, No Update (Over 15 Minutes)'})
