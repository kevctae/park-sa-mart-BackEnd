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
        return jsonify(result)
    else:
        mysql.connection.commit()
        cur.close()
        return jsonify({'message' : 'NO_CURRENT_PAKRING_SESSION_FOUND'})
        

