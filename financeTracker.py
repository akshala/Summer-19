from flask import Flask, render_template, jsonify, abort, make_response
from flask import request, url_for
from flask_restful import Resource, Api
from flask_httpauth import HTTPBasicAuth
import mysql.connector
import mysql
import json
import datetime

auth = HTTPBasicAuth()
app = Flask(__name__)

mydb = mysql.connector.connect(
	host="localhost",
	user="",
	passwd="",
	database="mydb",

)

mycursor = mydb.cursor()

@app.route('/moneymanager/expenditurerecords/<int:record_id>', methods=['GET']) # get data of a particular record id
@auth.login_required
def getData(record_id):
	record_id = int(record_id)
	# print(request.args)
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
@auth.login_required
def createData():
	description = request.args.get('description','')
	expenditure = float(request.args.get('expenditure',''))
	category = request.args.get('category','')
	date = request.args.get('date','')
	date_str = "STR_TO_DATE(\"{}\", \"%Y-%m-%d\")".format(date)
	# date = date.split('-')
	# year = int(date[0])
	# month = int(date[1])
	# day = int(date[2])
	# dateTime = str(datetime.date(year, month, day))
	# print(dateTime)

	sql_cmd = "INSERT INTO expenditure_records(description, expenditure, category, date) VALUE(\'{}\', {}, \'{}\', {})".format(description, expenditure, category, date_str)
	print(sql_cmd)
	mycursor.execute(sql_cmd)
	mydb.commit()
	return jsonify('ADDED')


@app.route('/moneymanager/expenditurerecords', methods=['GET']) #returns the entire database
@auth.login_required
def get_allData():
	category = request.args.get('category','')
	description = request.args.get('description','')
	date = request.args.get('date','') 
	# print(request.args, value)
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
	print(sql_cmd)
	mycursor.execute(sql_cmd)
	data = mycursor.fetchall()
	allData = []
	for entries in data:
		# print(entries)
		result = {
			'id': int(entries[0]),
			'description': entries[1],
			'expenditure': int(entries[2]),
			'category': entries[3],
			'date': str(entries[4])
		}
		# print(result)
		allData.append(result)
	return jsonify(allData)


@auth.get_password
def get_password(username):
    if username == 'akshala':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

if __name__ == "__main__":
    app.run()
