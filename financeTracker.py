from flask import Flask, render_template, jsonify, abort, make_response
from flask import request, url_for
from flask import request, current_app
from flask_restful import Resource, Api
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
import mysql.connector
import mysql
import json
from datetime import timedelta
from functools import update_wrapper

auth = HTTPBasicAuth()
app = Flask(__name__)
api = Api(app)
CORS(app, support_credentials=True)

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, str):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, str):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

@app.after_request
def after_request(response):
	response.headers.add('Access-Control-Allow-Origin', '*')
	response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
	response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
	return response

mydb = mysql.connector.connect(
	host="localhost",
	user="akshala",
	passwd="project",
	database="mydb",

)

mycursor = mydb.cursor()

@app.route("/")
def getPage():
    return render_template('dataPage.html')

@app.route('/moneymanager/expenditurerecords/<int:record_id>', methods=['GET', 'OPTIONS']) # get data of a particular record id
# @auth.login_required
def getData(record_id):
	record_id = int(record_id)
	sql_cmd = "SELECT * FROM expenditure_records WHERE id={}".format(record_id)
	mycursor.execute(sql_cmd)
	data = mycursor.fetchall() # data comes in the form of a list 
	for entries in data:
		print(entries)
		result = {
			'id': int(entries[0]),
			'description': entries[1],
			'expenditure': int(entries[2]),
			'category': entries[3],
			'date': str(entries[4])
		}
	return jsonify(result) # returning json string containing all information regarding a particular entry


@app.route('/moneymanager/expenditurerecords', methods=['POST'])
# @auth.login_required
def createData():
	description = request.args.get('description','')
	expenditure = float(request.args.get('expenditure',''))
	category = request.args.get('category','')
	date = request.args.get('date','')
	date_str = "STR_TO_DATE(\"{}\", \"%Y-%m-%d\")".format(date)

	sql_cmd = "INSERT INTO expenditure_records(description, expenditure, category, date) VALUE(\'{}\', {}, \'{}\', {})".format(description, expenditure, category, date_str)
	print(sql_cmd)
	mycursor.execute(sql_cmd)
	mydb.commit()
	return jsonify('ADDED')


@app.route('/moneymanager/expenditurerecords', methods=['GET'])
# @auth.login_required
def get_allData():
	category = request.args.get('category', '')
	description = request.args.get('description', '')
	date = request.args.get('date', '') 
	sql_cmd = ''
	if(category == '' and description == '' and date == ''):
		sql_cmd += "SELECT * FROM expenditure_records"
	else:
		if(category):
			sql_cmd += "SELECT * FROM expenditure_records WHERE category=\'{}\'".format(category)
		if(description):
			sql_cmd += "AND description=\'{}\'".format(description)
		if(date):
			sql_cmd += "AND date=\'{}\'".format(date)
	mycursor.execute(sql_cmd)
	data = mycursor.fetchall()
	allData = []
	for entries in data:
		result = {
			'id': int(entries[0]),
			'description': entries[1],
			'expenditure': int(entries[2]),
			'category': entries[3],
			'date': str(entries[4])
		}
		allData.append(result)
	return jsonify(allData)


# @auth.get_password
def get_password(username):
    if username == 'akshala':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

if __name__ == "__main__":
    app.run()