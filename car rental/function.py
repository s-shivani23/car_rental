import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import flash, request
import datetime
from datetime import timedelta
import json



@app.route('/search/<string:duration_from>,<string:duration_to>',methods=['GET'])

def available(duration_from,duration_to):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		print(duration_from)
		print(duration_to)
		cursor.execute("SELECT * FROM car WHERE car_id not in (SELECT car_id FROM booking_details WHERE duration_from<= %s && duration_to>= %s)",(duration_from,duration_to))
		empRows = cursor.fetchall()
		respone = jsonify(empRows)
		respone.status_code = 200
		
		
		
		return respone
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()


@app.route('/check_car/<string:duration_from>,<string:duration_to>,<int:car_id>',methods=['GET'])

def check_availablity(duration_from,duration_to,car_id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		print(duration_from)
		print(duration_to)
		cursor.execute("SELECT DISTINCT car_id FROM booking_details WHERE duration_from>= %s && duration_to<= %s && car_id=%s",(duration_from,duration_to,car_id))
		empRows = cursor.fetchall()
		respone = jsonify(empRows)
		respone.status_code = 200
		#res=respone.data.decode('utf-8')
		#print(json.loads(res)[0]["car_id"])
		
		
		
		return respone
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()



@app.route('/calculate/<string:duration_from>,<string:duration_to>,<int:car_id>',methods=['GET'])

def total_price(duration_from,duration_to,car_id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		datetimeFormat = '%Y-%m-%d %H:%M:%S'
		date1 = duration_from
		date2=duration_to
		
		diff = datetime.datetime.strptime(date2, datetimeFormat)\
						- datetime.datetime.strptime(date1, datetimeFormat)
		
		hrs_diff=diff.days * 24 + diff.seconds/3600
		#print(hrs_diff)
		
		
		
		
		cursor.execute("SELECT pph from car where car_id=%s",(car_id))
		empRows = cursor.fetchall()
		
		result=empRows[0]["pph"]
		val=int(result)* int(hrs_diff)
		#print(val)
		respone = jsonify(val)
		#print(respone.data.decode('utf-8'))
		respone.status_code = 200
		
		
		
		return respone
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/user/bookings/<int:user_id>',methods=['GET'])

def car_list(user_id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		
	
		cursor.execute("SELECT * FROM booking_details WHERE user_id=%s",(user_id))
		empRows = cursor.fetchall()
		respone = jsonify(empRows)
		respone.status_code = 200
		
		
		
		return respone
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()


@app.route('/car/bookings/<int:car_id>',methods=['GET'])

def user_list(car_id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
	
		cursor.execute("SELECT * FROM booking_details WHERE car_id=%s",(car_id))
		empRows = cursor.fetchall()
		respone = jsonify(empRows)
		respone.status_code = 200
		
		
		
		return respone
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()


@app.route('/car/book/', methods=['POST'])
def book_car():
	try:
		_json = request.json
		_user_id = _json['user_id']
		_car_id = _json['car_id']
		_duration_from = _json['duration_from']
		_duration_to=_json['duration_to']


		cars=check_availablity(_duration_from,_duration_to,_car_id)
		res=cars.data.decode('utf-8')
		#print(len(res))
		#print(res)
		if len(res) == 3:
					
															_res=total_price(_duration_from,_duration_to,_car_id)
															_cost=_res.data.decode('utf-8')
															if _user_id and _car_id and _duration_from and _duration_to and _cost and request.method == 'POST':         
																			sqlQuery = "INSERT INTO booking_details(user_id, car_id, duration_from,duration_to,total_price) VALUES(%s, %s, %s,%s,%s)"                                 
																			bindData = (_user_id, _car_id, _duration_from,_duration_to,_cost)
																			conn = mysql.connect()
																			cursor = conn.cursor()
																			cursor.execute(sqlQuery,bindData)
																			conn.commit()
																			respone = jsonify('Booking successfull!')
																			respone.status_code = 200
																			return respone
					
		else:
			return print("booking unsuccessful")
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()





if __name__ == "__main__":
	
	app.run()
