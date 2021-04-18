from app import *

def memberpaynow():
    try:
        email = request.json['email']
        parking_id = request.json['parking_id']
    except:
        return jsonify({'message' : 'BAD_PAYLOAD'}) , 400
    cur = mysql.connection.cursor()
    token = generate_token(email)
    checkValue = cur.execute('SELECT * FROM Parking_record WHERE parking_id = %s and parking_id NOT IN (select parking_id from Invoice)', (parking_id,))
    if checkValue > 0:
        result = cur.fetchone()
        now = datetime.datetime.now(tz)
        time_delta = (now - result['entry_datetime'])
        total_seconds = time_delta.total_seconds()
        minutes = total_seconds/60
        if minutes < 15:
            parking_cost = 0
        else:
            hours = math.ceil(minutes/60)
            parking_cost = 15 * hours
        cur.fetchall()
        cur.execute('SELECT main_payment_method,wallet FROM Account WHERE email = %s', (email,))
        token = cur.fetchone()
        if token['main_payment_method'] == 'VISA':
            cur.execute('INSERT INTO Invoice(amount,method,payment_datetime,parking_id) VALUES(%s,%s,%s,%s)',(parking_cost,token['main_payment_method'],now,parking_id,))
            mysql.connection.commit()
            cur.close()
            return jsonify({'payment_datetime' : now, 'amount' : parking_cost, 'method' : token['main_payment_method']}) ,201
        else:
            if token['wallet'] < parking_cost:
                mysql.connection.commit()
                cur.close()
                return jsonify({'message' : 'WALLET_MONEY_NOT_SUFFICIENT'}) ,409
            else:
                token['wallet'] = token['wallet'] - parking_cost
                cur.execute('UPDATE Account SET wallet = %s WHERE email = %s' , (token['wallet'],email,))
                cur.execute('INSERT INTO Invoice(amount,method,payment_datetime,parking_id) VALUES(%s,%s,%s,%s)',(parking_cost,token['main_payment_method'],now,parking_id,))
                mysql.connection.commit()
                cur.close()
                return jsonify({'payment_datetime' : now, 'amount' : parking_cost, 'method' : token['main_payment_method']}) ,201
    else:
        mysql.connection.commit()
        cur.close()
        return jsonify({'message' : 'PARKING_FEE_IS_PAID'}) ,409