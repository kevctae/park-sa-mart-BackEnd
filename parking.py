from app import *

def currentparkingsession():
    email = request.json['email']
    cur = mysql.connection.cursor()
    token = generate_token(email)
    checkValue = cur.execute('SELECT parking_id,entry_datetime,building,floor,entry_picture,parking_platenum,parking_platecity FROM Parking_record WHERE email = %s and exit_datetime IS NULL', (email,))
    if checkValue > 0:
        result = cur.fetchone()
        now = datetime.datetime.now()
        time_delta = (now - result['entry_datetime'])
        total_seconds = time_delta.total_seconds()
        minutes = total_seconds/60
        if minutes < 15:
            parking_cost = 0
        else:
            hours = math.ceil(minutes/60)
            parking_cost = 15 * hours
        cur.fetchall()
        cur.execute('SELECT brand,model FROM Cars WHERE platenum = %s and platecity = %s', (result['parking_platenum'],result['parking_platecity'],))
        car_info = cur.fetchone()
        result['brand'] = car_info['brand']
        result['model'] = car_info['model']
        result['parking_cost'] = parking_cost
        cur.fetchall()
        checkStatusValue = cur.execute('SELECT invoice_id FROM Invoice WHERE parking_id = %s', (result['parking_id'],))
        if checkStatusValue == 0:
            result['payment_status'] = False
        else:
            result['payment_status'] = True
        result['token'] = token
        result['expiresIn'] = '600'
        result['email'] = email
        mysql.connection.commit()
        cur.close()
        return jsonify(result), 200
    else:
        mysql.connection.commit()
        cur.close()
        return jsonify({'message' : 'NO_CURRENT_PAKRING_SESSION_FOUND'}), 200

def getavailableparkingspace():
    cur = mysql.connection.cursor()
    cur.callproc('Find_available_space');
    result = cur.fetchall()
    cur.close()
    return jsonify(result)
        
def recordcarentry(entry_picture,building,floor,parking_platenum,parking_platecity,entry_datetime):
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
        return jsonify({'message' : 'Success'}) , 200
    except:
        return jsonify({'message' : 'Failed, Cannot Insert Into DB'}) , 400

def updatecarfloor(building,floor,parking_platenum,parking_platecity,update_datetime):
    cur = mysql.connection.cursor()
    checkValue = cur.execute('SELECT * FROM Parking_record WHERE parking_platenum = %s and parking_platecity = %s and parking_id not in (select parking_id from Invoice)', (parking_platenum,parking_platecity,))
    if checkValue == 0:
        mysql.connection.commit()
        cur.close()
        return jsonify({'message' : 'Success'}) , 200
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
        return jsonify({'message' : 'Success, Updated'}) ,200
    mysql.connection.commit()
    cur.close()
    return jsonify({'message' : 'Success, No Update (Over 15 Minutes)'}) , 200
