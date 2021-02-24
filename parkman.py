from app import *

def visitorentry():
    plate=request.json['plate']
    entrydatetime=request.json['entrydatetime']
    cur = mysql.connection.cursor()
    checkValue = cur.execute ('SELECT plate FROM cars WHERE plate=%s', (plate,))
    for i in checkValue:
        string=checkValue[i]
    if checkValue == 0:
        return "Plate not found"
    else:
    detail = cur.execute ('SELECT entrytime,floor,image FROM parking_record WHERE entrytime=%s AND floor=%s AND image=%s', (entrytime,floor,image,))
    return jsonify?????