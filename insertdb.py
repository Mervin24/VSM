from flask import Flask,jsonify,request,render_template
from flask.ext.mysql import MySQL
import csv
import numpy as np
import random as rand
from random import *
import matplotlib.pyplot as plt

app = Flask(__name__)
mysql = MySQL()
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'vsm'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

	

conn = mysql.connect()
cursor=conn.cursor()
@app.route("/insert",methods=['GET', 'POST'])	
def inesrt():
	count =0;
	with open('company_names1.csv', 'r') as csvfile:
		csvreader = csv.reader(csvfile)
		for row in csvreader:
			print("INSERT INTO `company` (`CompanyId`, `CompanyName`, `Volume`, `Price`) VALUES ('"+str(row[1])+"', '"+str(row[0])+"', '"+str(randint(500,2000))+"', '"+str(randint(500,2000))+"')")
			print(count)
			cursor.execute("INSERT INTO `company` (`CompanyId`, `CompanyName`, `Volume`, `Price`) VALUES ('"+str(row[1])+"', '"+str(row[0])+"', '"+str(randint(500,2000))+"', '"+str(randint(500,2000))+"');")
			conn.commit()
			count=count+1
			if count == 100:
				return "done"
	return 'Tr'

@app.route("/createcsv",methods=['GET', 'POST'])	
def createCsv():
	cursor=conn.cursor()
	cursor.execute("SELECT * FROM `company` ;")
	result=cursor.fetchall()
	print(type(result))
	for i in result :
		name = i[0]+".csv"
		f = open(name,'w+')
		f.close()
	return 'tr'

@app.route("/getcsv",methods=['GET', 'POST'])	
def getcsv():
	cursor=conn.cursor()
	for i in range(50):
		cursor.execute("SELECT * FROM `company` ;")
		result=cursor.fetchall()
		print(type(result))
		for i in result :
			name = i[0]+".csv"
			f = open(name,'r')
			list = f.readlines()
			f.close()
			f = open(name,'w')
			if list==[]:
				element = "0,"+str(i[3])
				f.write(str(element))
				#print("e")
			else:
				count = len(list)
				new_element = "\n"+str(count)+","+str(i[3])
				list.append(new_element)
				for i in list:
					f.write(str(i))
				print(count)
			f.close()
			print(i)
		for i in result :	
			cursor.execute("UPDATE company SET Price = '"+str(int(i[3]+i[3]*rand.uniform(-0.01,0.01)))+"' WHERE CompanyId = '"+str(i[0])+"'")
			print ("changed"+str(i[3])+" "+str(int(i[3]+i[3]*rand.uniform(-0.01,0.01))))
			conn.commit()
	return 'Tr'
	
@app.route("/plot",methods=['GET', 'POST'])	
def plot():
	cursor=conn.cursor()
	cursor.execute("SELECT * FROM `company` ;")
	result=cursor.fetchall()
	print(type(result))
	count = 0
	x = []
	y = []
	for i in result :
		print(count)
		count+=1
		name = i[0]+".csv"
		
		x.clear()
		y.clear()
		with open(name, 'r') as csvfile:
			plots= csv.reader(csvfile, delimiter=',')
			for row in plots:
				x.append(int(row[0]))
				y.append(int(row[1]))	
		print(len(y))		
		plt.plot(x, y, color='g')
		plt.xlabel('Days')
		plt.ylabel('Price')
		
		plt.title('Stock Value')
		png_name = i[0]+".png"
		plt.savefig(png_name)
		plt.gcf().clear()
			
	return 'plotted'
	

	
if __name__ == "__main__":
	app.run(host="0.0.0.0",port=5060,debug=True)
	
	
	