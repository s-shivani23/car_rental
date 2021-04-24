import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import flash, request



@app.route('/add', methods=['POST'])
def add_user():
	try:
		_json = request.json
		_user_id = _json['user_id']
		_name = _json['name']
		_phone_number = _json['phone_number']
		
        	
		if _user_id and _name and _phone_number  and request.method == 'POST':			
			sqlQuery = "INSERT INTO user(user_id, name, phone_number) VALUES(%s, %s, %s)"
			bindData = (_user_id, _name, _phone_number)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sqlQuery,bindData)
			conn.commit()
			respone = jsonify('User added successfully!')
			respone.status_code = 200
			return respone
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/user')
def user():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT user_id, name, phone_number FROM user")
		Rows = cursor.fetchall()
		respone = jsonify(Rows)
		respone.status_code = 200
		return respone
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/update', methods=['PUT'])
def update_user():
            try:
                    _json = request.json
                    _user_id = _json['user_id']
                    _name = _json['name']
                    _phone_number = _json['phone_number']
                        
                        
                    if _user_id and _name and _phone_number and request.method == 'PUT':			
                        sqlQuery = "UPDATE user SET name=%s, phone_number=%s WHERE user_id=%s"
                        bindData = (_user_id,_name,_phone_number)
                        conn = mysql.connect()
                        cursor = conn.cursor()
                        cursor.execute(sqlQuery, bindData)
                        conn.commit()
                        respone = jsonify('Employee updated successfully!')
                        respone.status_code = 200
                        return respone
                    else:
                        return not_found()	
            except Exception as e:
                         print(e)
            finally:
                     cursor.close() 
                     conn.close()

		 
@app.route('/delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM user WHERE user_id =%s", (user_id))
		conn.commit()
		respone = jsonify('Employee deleted successfully!')
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
