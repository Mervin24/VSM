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
import hashlib

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



'''def foo():
	while True:
		time.sleep(180)
		getcsv()'''	

def getcsv():
	cursor=conn.cursor()
	cursor.execute("SELECT * FROM `company`;")
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
	
	return 'True'
	
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
	cursor.execute("SELECT username From users WHERE username = '"+Username+"';")
	result = cursor.fetchone()
	if(result is not None):
		return render_template('signup.html')
	hash_object_password = hashlib.md5(password.encode())
	print(password)
	print(hash_object_password.hexdigest())
	password = hash_object_password.hexdigest()
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
	hash_object_password = hashlib.md5(password.encode())
	print(hash_object_password.hexdigest())
	password = hash_object_password.hexdigest()
	cursor.execute("SELECT `password` FROM `users` WHERE username='"+username+"' ;")
	result = cursor.fetchone()
	if(result is None):
		return render_template("login.html")
	if(result[0]==password):
		cursor.execute("SELECT username,Cash FROM `users` WHERE username='"+username+"' ;")
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
	cursor.execute("SELECT Headline FROM news;")
	result = cursor.fetchall()
	return render_template('homepage.html',result = result)
	
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
	cursor=conn.cursor()
	username = ""
	if request.method == 'POST':
		username = request.form["username"]
	print(username)
	cursor.execute("SELECT TransactionId,CompanyId ,sum(Volume) FROM `transactions` WHERE username='"+username+"' GROUP BY CompanyId;")
	result=cursor.fetchall()
	arr = []
	print(result)
	for i in result:
		if i[2]==0:
			print("removed "+i[1])
			lis = list(result)
			lis.remove(i)
			result = tuple(lis)
			continue
		cursor.execute("SELECT Price FROM `company` WHERE CompanyId='"+i[1]+"';");
		arr.append(cursor.fetchone())
	print(arr)
	sum = 0
	for i in range(len(result)):
		sum += int(result[i][2]) * (arr[i][0])
	print(sum)
	return render_template("myHoldings.html",result = result, arr = arr, sum = sum)

@app.route("/leaderboard",methods=['GET', 'POST'])	
def leaderboard():	
	cursor.execute("SELECT username,Cash FROM users ORDER BY Cash DESC");
	result = cursor.fetchall()
	for i in result:
		print(i[1])
	return render_template("leaderboard.html",result=result)
	
@app.route("/stylesheet",methods=['GET', 'POST'])	
def stylesheet():	
	return render_template("myHoldingcssfile.css")

	
@app.route("/clearCookies",methods=['GET', 'POST'])	
def clearCookies():	
	return render_template("clearCookies.html")

@app.route("/sendUserName",methods=['GET', 'POST'])	
def sendUserName():	
	return render_template("sendUserName.html")

	
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
	cursor.execute("UPDATE users SET cash='"+moneyLeft+"' WHERE username='"+username+"';")
	cursor.execute("UPDATE company SET Volume='"+sharesLeft+"' WHERE CompanyId='"+cid+"';")
	cursor.execute("INSERT INTO `transactions` (`username`, `CompanyId`, `Volume`) VALUES ( '"+username+"', '"+cid+"', '"+shares+"');")
	
	#cursor.execute()
	
	conn.commit();
	
	print("updated")
	return company()


@app.route("/sell",methods=['GET', 'POST'])	
def sell():
	username = request.form["username"]
	shares = request.form["shares"]
	cid = request.form["company_id"]
	moneyLeft = request.form["moneyLeft"]
	
	print(username)
	print(shares)
	print(moneyLeft)
	print(cid)
	cursor.execute("SELECT Volume FROM company WHERE CompanyId='"+cid+"';")
	sharesLeft = cursor.fetchone()
	sharesLeft = sharesLeft[0]
	print("before shares "+str(sharesLeft))
	sharesLeft = int(sharesLeft)+ int(shares)
	print("updated shares "+str(sharesLeft))
	cursor.execute("UPDATE users SET cash='"+moneyLeft+"' WHERE username='"+username+"';")
	cursor.execute("UPDATE company SET Volume='"+str(sharesLeft)+"' WHERE CompanyId='"+cid+"';")
	cursor.execute("INSERT INTO `transactions` (`username`, `CompanyId`, `Volume`) VALUES ( '"+username+"', '"+cid+"', '-"+shares+"');")
	
	#cursor.execute()
	
	conn.commit();
	
	print("updated")
	return company()
	
	
	


'''timerThread = threading.Thread(target=foo)
timerThread.daemon = True
timerThread.start()'''
	
if __name__ == "__main__":
	app.run(host="0.0.0.0",port=5050,debug=True)