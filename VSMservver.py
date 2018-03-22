imofrom flask import Flask,jsonify,request

app = Flask(__name__)

db = MySQLdb.connect("localhost", "root", "", "vsm")
cursor=db.cursor()

@app.route("/signup",methods=["GET","POST"])
def Signup():
	cursor.execute("")
if __name__ == "__main__":
	app.run(host="0.0.0.0",port=5050,debug=True)