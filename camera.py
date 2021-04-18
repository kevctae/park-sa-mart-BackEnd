from app import *
import parking

def carentry():
    try:
        entry_picture = request.json['entry_picture']
        building = request.json['building']
        floor = request.json['floor']
        parking_platenum = request.json['parking_platenum']
        parking_platecity = request.json['parking_platecity']
        entry_datetime = request.json['entry_datetime']
    except:
        return jsonify({'message' : 'Failed'}) , 400
    return parking.recordcarentry(entry_picture,building,floor,parking_platenum,parking_platecity,entry_datetime)
    
def updatecarfloor(): 
    try:
        building = request.json['building']
        floor = request.json['floor']
        parking_platenum = request.json['parking_platenum']
        parking_platecity = request.json['parking_platecity']
        update_datetime = request.json['update_datetime']
    except:
        return jsonify({'message' : 'Failed'}) , 400
    return parking.updatecarfloor(building,floor,parking_platenum,parking_platecity,update_datetime)
    

def carexit():
    try:
        exit_picture = request.json['exit_picture']
        parking_platenum = request.json['parking_platenum']
        parking_platecity = request.json['parking_platecity']
        exit_datetime = request.json['exit_datetime']
    except:
        return jsonify({'message' : 'Failed'})
    cur = mysql.connection.cursor()
    checkLegitValue = cur.execute('SELECT * FROM Parking_record WHERE parking_platenum = %s and parking_platecity = %s and exit_datetime IS NULL', (parking_platenum,parking_platecity,))
    if checkLegitValue == 0:
        return jsonify({'message' : 'LICENSE_PLATE_NOT_FOUND'})
    cur.fetchall()
    checkValue = cur.execute('SELECT email FROM Cars WHERE platenum = %s and platecity = %s', (parking_platenum,parking_platecity,))
    exit_datetime = datetime.datetime.strptime(exit_datetime, '%Y-%m-%d %H:%M:%S')
    if checkValue > 0: # is member
        temp = cur.fetchone()
        email = temp['email']
        cur.fetchall()
        checkPaymentValue = cur.execute('SELECT * FROM Parking_record WHERE parking_platenum = %s and parking_platecity = %s and exit_datetime IS NULL and parking_id  in (select parking_id from Invoice) ORDER BY parking_id DESC LIMIT 1', (parking_platenum,parking_platecity,))
        if checkPaymentValue > 0: # member already paid 
            result = cur.fetchone()
            cur.execute('SELECT * FROM Invoice WHERE parking_id = %s', (result['parking_id'],))
            invoice = cur.fetchone()
            now = datetime.datetime.now().replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Bangkok'))
            time_delta = (exit_datetime - invoice['payment_datetime'])
            total_seconds = time_delta.total_seconds()
            minutes = total_seconds/60
            if minutes < 15:
                cur.execute('UPDATE Parking_record SET exit_picture = %s, exit_datetime = %s WHERE parking_id = %s', (exit_picture,exit_datetime,result['parking_id'],))
                mysql.connection.commit()
                cur.close()
                return jsonify({'message' : 'Open Gate'})
            else:
                hours = math.ceil(minutes/60)
                additional_cost = 15 * hours
                cur.execute('UPDATE Parking_record SET exit_picture = %s, exit_datetime = %s WHERE parking_id = %s', (exit_picture,exit_datetime,result['parking_id'],))
                invoice['amount'] = invoice['amount'] + additional_cost
                cur.execute('UPDATE Invoice SET amount = %s WHERE invoice_id = %s', (invoice['amount'],invoice['invoice_id'],))
                mysql.connection.commit()
                cur.close()
                return jsonify({'message' : 'Please Collect Additional Cash Before Opening Gate', 'Amount' : additional_cost})
        else:  # member not paid
            cur.fetchall()
            cur.execute('SELECT * FROM Parking_record WHERE parking_platenum = %s and parking_platecity = %s and exit_datetime IS NULL and parking_id not in (select parking_id from Invoice) ORDER BY parking_id DESC LIMIT 1', (parking_platenum,parking_platecity,))
            result = cur.fetchone()
            now = datetime.datetime.now().replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Bangkok'))
            time_delta = (exit_datetime - result['entry_datetime'])
            total_seconds = time_delta.total_seconds()
            minutes = total_seconds/60
            parking_cost = 0
            if minutes < 15:
                parking_cost = 0
            else:
                hours = math.ceil(minutes/60)
                parking_cost = 15 * hours
            cur.execute('SELECT main_payment_method,wallet FROM Account WHERE email = %s', (email,))
            token = cur.fetchone()
            if token['main_payment_method'] == 'VISA':
                cur.execute('INSERT INTO Invoice(amount,method,payment_datetime,parking_id) VALUES(%s,%s,%s,%s)',(parking_cost,token['main_payment_method'],now,result['parking_id'],))
                cur.execute('UPDATE Parking_record SET exit_picture = %s, exit_datetime = %s WHERE parking_id = %s', (exit_picture,exit_datetime,result['parking_id'],))
                mysql.connection.commit()
                cur.close()
                return jsonify({'message' : 'Open Gate'})
            else: # member use wallet
                if token['wallet'] < parking_cost:
                    cur.execute('INSERT INTO Invoice(amount,method,payment_datetime,parking_id) VALUES(%s,%s,%s,%s)',(parking_cost,'Cash',now,result['parking_id'],))
                    cur.execute('UPDATE Parking_record SET exit_picture = %s, exit_datetime = %s WHERE parking_id = %s', (exit_picture,exit_datetime,result['parking_id'],))
                    mysql.connection.commit()
                    cur.close()
                    return jsonify({'message' : 'Please Collect Cash Before Opening Gate', 'Amount' : parking_cost})
                else:
                    token['wallet'] = token['wallet'] - parking_cost
                    cur.execute('UPDATE Account SET wallet = %s WHERE email = %s' , (token['wallet'],email,))
                    cur.execute('INSERT INTO Invoice(amount,method,payment_datetime,parking_id) VALUES(%s,%s,%s,%s)',(parking_cost,token['main_payment_method'],now,result['parking_id'],))
                    cur.execute('UPDATE Parking_record SET exit_picture = %s, exit_datetime = %s WHERE parking_id = %s', (exit_picture,exit_datetime,result['parking_id'],))
                    mysql.connection.commit()
                    cur.close()
                    return jsonify({'message' : 'Open Gate'})
    else: # is visitor
        checkPaymentValue = cur.execute('SELECT * FROM Parking_record WHERE parking_platenum = %s and parking_platecity = %s and exit_datetime IS NULL and parking_id  in (select parking_id from Invoice) ORDER BY parking_id DESC LIMIT 1', (parking_platenum,parking_platecity,))
        if checkPaymentValue > 0: # visitor already paid
            result = cur.fetchone()
            cur.execute('SELECT * FROM Invoice WHERE parking_id = %s', (result['parking_id'],))
            invoice = cur.fetchone()
            now = datetime.datetime.now().replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Bangkok'))
            time_delta = (exit_datetime - invoice['payment_datetime'])
            total_seconds = time_delta.total_seconds()
            minutes = total_seconds/60
            if minutes < 15:
                cur.execute('UPDATE Parking_record SET exit_picture = %s, exit_datetime = %s WHERE parking_id = %s', (exit_picture,exit_datetime,result['parking_id'],))
                mysql.connection.commit()
                cur.close()
                return jsonify({'message' : 'Open Gate'})
            else:
                hours = math.ceil(minutes/60)
                additional_cost = 15 * hours
                cur.execute('UPDATE Parking_record SET exit_picture = %s, exit_datetime = %s WHERE parking_id = %s', (exit_picture,exit_datetime,result['parking_id'],))
                invoice['amount'] = invoice['amount'] + additional_cost
                cur.execute('UPDATE Invoice SET amount = %s WHERE invoice_id = %s', (invoice['amount'],invoice['invoice_id'],))
                mysql.connection.commit()
                cur.close()
                return jsonify({'message' : 'Please Collect Additional Cash Before Opening Gate', 'Amount' : additional_cost})
        else:
            cur.fetchall()
            cur.execute('SELECT * FROM Parking_record WHERE parking_platenum = %s and parking_platecity = %s and exit_datetime IS NULL and parking_id not in (select parking_id from Invoice) ORDER BY parking_id DESC LIMIT 1', (parking_platenum,parking_platecity,))
            result = cur.fetchone()
            now = datetime.datetime.now().replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Bangkok'))
            time_delta = (exit_datetime - result['entry_datetime'])
            total_seconds = time_delta.total_seconds()
            minutes = total_seconds/60
            parking_cost = 0
            if minutes < 15:
                parking_cost = 0
            else:
                hours = math.ceil(minutes/60)
                parking_cost = 15 * hours
            cur.execute('INSERT INTO Invoice(amount,method,payment_datetime,parking_id) VALUES(%s,%s,%s,%s)',(parking_cost,'Cash',now,result['parking_id'],))
            cur.execute('UPDATE Parking_record SET exit_picture = %s, exit_datetime = %s WHERE parking_id = %s', (exit_picture,exit_datetime,result['parking_id'],))
            mysql.connection.commit()
            cur.close()
            return jsonify({'message' : 'Please Collect Cash Before Opening Gate', 'Amount' : parking_cost})