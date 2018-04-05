from flask import Flask,jsonify,request,render_template
from flask.ext.mysql import MySQL
from flask_mail import Mail, Message
from smtplib import SMTP
from flask import send_file

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




	
def getcsv():
	cursor=conn.cursor()
	
	cursor.execute("SELECT * FROM `company` ;")
	result=cursor.fetchall()
	print(type(result))
	for i in result :
		name = "/static/data/"+i[0]+".csv"
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
		name = "/static/data/"+i[0]+".csv"
		
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
		png_name = "/static/images/"+i[0]+".png"
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
		return render_template('homepage.html')
	else:
		return render_template("login.html")
	
@app.route("/navbar",methods=['GET', 'POST'])	
def navbar():	
	return render_template("navbar.html")
	
@app.route("/homepage",methods=['GET', 'POST'])	
def homepage():	
	return render_template("homepage.html")
	
@app.route("/company",methods=['GET', 'POST'])	
def company():	
	cursor=conn.cursor()
	cursor.execute("SELECT * FROM `company` ;")
	result=cursor.fetchall()
	result = str(result)
	result = result.replace("'","")
	result = result.replace("(","")
	
	result = result[0:len(result)-2]
	print(result)
	return render_template("company.html", result = result )
	
@app.route("/myHoldings",methods=['GET', 'POST'])	
def myHoldings():	
	return render_template("myHoldings.html")

@app.route("/leaderboard",methods=['GET', 'POST'])	
def leaderboard():	
	return render_template("leaderboard.html")
	
@app.route("/stylesheet",methods=['GET', 'POST'])	
def stylesheet():	
	return render_template("myHoldingcssfile.css")



	
if __name__ == "__main__":
	app.run(host="0.0.0.0",port=5050,debug=True)