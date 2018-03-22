imofrom flask import Flask,jsonify,request

app = Flask(__name__)

db = MySQLdb.connect("localhost", "root", "", "vsm")
cursor=db.cursor()

INSERT INTO `users` (`username`, `password`, `phone_number`, `email`, `name`, `id_num`) VALUES ('Mervin24', 'deep1BC', '8974561230', 'mdalmet@gmail.com', 'Mervin Dalmet', NULL);

@app.route("/signup",methods=["GET","POST"])
def Signup():
	firstName = request.form["firstName"]
	lastName = request.form["lastName"]
	Username = request.form["username"]
	password = request.form["pass"]
	contact = request.form["contact"]
	id_num = request.form["id"]
	email = request.form["email"]
	
	cursor.execute("")
if __name__ == "__main__":
	app.run(host="0.0.0.0",port=5050,debug=True)