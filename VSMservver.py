from flask import Flask,jsonify,request,render_template,Response,redirect
from flask.ext.mysql import MySQL
from flask_mail import Mail, Message
from smtplib import SMTP
from flask import send_file
from apscheduler.schedulers.background import BackgroundScheduler
import random as rand
from random import *
import matplotlib.pyplot as plt
import csv
import numpy as np
import time, threading
import json

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

#INSERT INTO `users` (`username`, `password`, `phone_number`, `email`, `name`, `id_num`) VALUES ('Mervin24', 'deep1BC', '8974561230', 'mdalmet@gmail.com', 'Mervin Dalmet', NULL);

'''def sensor():
    """ Function for test purposes. """
    getcsv()
    plot()
    print("Companies updated")

sched = BackgroundScheduler(daemon=True)
sched.add_job(sensor,'interval',minutes=2)
sched.start()
'''

'''def foo():
	while True:
		time.sleep(120)
		getcsv()	'''	

def getcsv():
	cursor=conn.cursor()
	
	cursor.execute("SELECT * FROM `company` ;")
	result=cursor.fetchall()
	print(type(result))
	for i in result :
		name = "static/data/"+i[0]+".csv"
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
			for j in list:
				f.write(str(j))
			print(count)
		f.close()
		print(j)
	for i in result :	
		cursor.execute("UPDATE company SET Price = '"+str(int(i[3]+i[3]*rand.uniform(-0.01,0.01)))+"' WHERE CompanyId = '"+str(i[0])+"'")
		print ("changed"+str(i[3])+" "+str(int(i[3]+i[3]*rand.uniform(-0.01,0.01))))
		conn.commit()
		
	plot()
	return 'Tr'
	
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
		name = "static/data/"+i[0]+".csv"
		
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
		
		plt.title(str(i[1]))
		png_name = "static/images/"+i[0]+".png"
		plt.savefig(png_name)
		plt.gcf().clear()
		
	return 'plotted'






@app.route("/")
def index():
	return render_template('login.html')
	
@app.route("/signupPage")
def signupPage():
	return render_template('signup.html')
	

@app.route("/signup",methods=['GET', 'POST'])
def Signup():
	#print("hello")
	firstName = request.form["firstName"]
	lastName = request.form["lastName"]
	Username = request.form["username"]
	password = request.form["pass"]
	contact = request.form["contact"]
	id_num = request.form["id"]
	email = request.form["email"]
	cursor.execute("INSERT INTO `users` (`username`, `password`, `phone_number`, `email`, `name`) VALUES ('"+Username+"', '"+password+"', '"+contact+"', '"+email+"', '"+firstName+" "+lastName+"');")
	conn.commit()
	return render_template("login.html")

@app.route("/login",methods=['GET', 'POST'])	
def login():
	print("hi")
	cursor=conn.cursor()
	username = request.form["username"]
	password = request.form["password"]
	print(password)
	cursor.execute("SELECT `password` FROM `users` WHERE username='"+username+"' ;")
	result = cursor.fetchone()
	print(str(result[0]))
	if(result[0]==password):
		cursor.execute("SELECT username,Cash,stock FROM `users` WHERE username='"+username+"' ;")
		result = cursor.fetchall()
		print(result)
		return render_template('cookies.html',result=result)
	else:
		return render_template("login.html")
	
@app.route("/navbar",methods=['GET', 'POST'])	
def navbar():	
	return render_template("navbar.html")
	
@app.route("/homepage",methods=['GET', 'POST'])	
def homepage():	
	return render_template('homepage.html')
	
@app.route("/company",methods=['GET', 'POST'])	
def company():	
	cursor=conn.cursor()
	cursor.execute("SELECT * FROM `company` ;")
	result=cursor.fetchall()
	'''result = str(result)
	result = result.replace("'","")
	result = result.replace("(","")
	
	result = result[0:len(result)-2]
	print(result)'''
	return render_template("company.html", result = result )
	
@app.route("/companyProfile/<ID>",methods=['GET', 'POST'])	
def companyProfile(ID):
	print(ID)
	cursor.execute("SELECT CompanyName,Volume,Price FROM `company` WHERE CompanyId = '"+ID+"';")
	result = cursor.fetchall()
	
	
	return render_template("companyProfile.html",result = result,ID = ID)
	
@app.route("/myHoldings",methods=['GET', 'POST'])	
def myHoldings():	
	return render_template("myHoldings.html")

@app.route("/leaderboard",methods=['GET', 'POST'])	
def leaderboard():	
	return render_template("leaderboard.html")
	
@app.route("/stylesheet",methods=['GET', 'POST'])	
def stylesheet():	
	return render_template("myHoldingcssfile.css")

	
@app.route("/clearCookies",methods=['GET', 'POST'])	
def clearCookies():	
	return render_template("clearCookies.html")


@app.route("/buy",methods=['GET', 'POST'])	
def buy():
	username = request.form["username"]
	shares = request.form["shares"]
	cid = request.form["company_id"]
	money = request.form["money"]
	sharesLeft = request.form["sharesLeft"]
	moneyLeft = request.form["moneyLeft"]
	
	print(username)
	print(shares)
	print(money)
	print(cid)
	price = int(int(money)/int(shares))
	print(price)
	cursor.execute("UPDATE users SET cash='"+moneyLeft+"' WHERE username='"+username+"';")
	cursor.execute("UPDATE company SET Volume='"+sharesLeft+"' WHERE CompanyId='"+cid+"';")
	cursor.execute("INSERT INTO `transactions` (`username`, `CompanyId`, `Volume`, `Price`) VALUES ( '"+username+"', '"+cid+"', '"+shares+"', '"+str(price)+"');")
	
	#cursor.execute()
	
	conn.commit();
	
	print("updated")
	return company()




'''timerThread = threading.Thread(target=foo)
timerThread.daemon = True
timerThread.start()'''

	
if __name__ == "__main__":
	app.run(host="0.0.0.0",port=5050,debug=True)