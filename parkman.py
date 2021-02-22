from app import *

def visitorentry():
    plate=request.json['plate']
    entrydatetime=request.json['entrydatetime']
    cur = mysql.connection.cursor()
    checkValue = cur.execute ('SELECT plate FROM cars WHERE plate=%s', (plate,))
    if checkValue == 0:
        return "Plate not found"
    else:
        



