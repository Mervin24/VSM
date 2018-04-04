from flask import Flask,jsonify,request,render_template
from flask.ext.mysql import MySQL
from flask_mail import Mail, Message
from smtplib import SMTP

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
	return render_template("company.html")
	
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