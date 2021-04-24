import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import flash, request

@app.route('/add_car', methods=['POST'])
def add_car():
	try:
		_json = request.json
		_car_id=_json['car_id']
		_car_liscence_number = _json['car_liscence_number']
		_manufacturer = _json['manufacturer']
		_model = _json['model']
		_base_price = _json['base_price']
		_pph = _json['pph']
		_security_deposit=_json['security_deposit']
		
        	
		if _car_id and _car_liscence_number and _manufacturer and _model and _base_price and _pph and _security_deposit and request.method == 'POST':			
			sqlQuery = "INSERT INTO car(car_id,car_liscence_number, manufacturer, model,base_price,pph,security_deposit) VALUES(%s, %s, %s,%s,%s,%s)"
			bindData = (_car_id,_car_liscence_number, _manufacturer, _model,_base_price,_pph,_security_deposit)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sqlQuery,bindData)
			conn.commit()
			respone = jsonify('Car added successfully!')
			respone.status_code = 200
			return respone
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
@app.route('/car')
def car():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT car_id,car_liscence_number, manufacturer, model,base_price, pph, security_deposit FROM car")
		empRows = cursor.fetchall()
		respone = jsonify(empRows)
		respone.status_code = 200
		return respone
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/update_car', methods=['PUT'])
def update_car():
            try:
                    _json = request.json
                    _car_id=_json['car_id']
                    _car_liscence_number = _json['car_liscence_number']
                    _manufacturer = _json['manufacturer']
                    _model = _json['model']
                    _base_price = _json['base_price']
                    _pph = _json['pph']
                    _security_deposit=_json['security_deposit']                        
                    if _car_id and _car_liscence_number and _manufacturer and _model and _base_price and _pph and _security_deposit and request.method == 'PUT':			
                        sqlQuery = "UPDATE car SET car_liscence_number=%s,manufacturer=%s, model=%s,base_price=%s,pph=%s,security_deposit=%s WHERE car_id=%s"
                        bindData = (_car_id,_car_liscence_number,_manufacturer,_model,_base_price,_pph,_security_deposit)
                        conn = mysql.connect()
                        cursor = conn.cursor()
                        cursor.execute(sqlQuery, bindData)
                        conn.commit()
                        respone = jsonify('Car updated successfully!')
                        respone.status_code = 200
                        return respone
                    else:
                        return not_found()	
            except Exception as e:
                         print(e)
            finally:
                     cursor.close() 
                     conn.close()

                     
@app.route('/delete_car/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM car WHERE car_id =%s", (car_id))
		conn.commit()
		respone = jsonify('Car deleted successfully!')
		respone.status_code = 200
		return respone
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone



if __name__ == "__main__":
    
    app.run()
