from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail,Message
import mysql.connector

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/userdata'
db = SQLAlchemy(app)

app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'avinashkumaryadav0622@gmail.com',
	MAIL_PASSWORD = '8294391578'
	)

mail=Mail(app)

mydb=mysql.connector.connect(host="localhost", user="root", database="userdata")

class project(db.Model):
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    mobileNo = db.Column(db.Integer)
    password = db.Column(db.String(100), unique=True, nullable=False)



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signup")
def index1():
    return render_template("signup.html")

@app.route("/submit",methods=["post"])
def submit():
    email=request.form.get("email")
    password=request.form.get("password")
    mobileNo=request.form.get("MobileNo")
    mycursor=mydb.cursor()
    sql="select * from project where email='"+email+"'"
    mycursor.execute(sql)
    data=mycursor.fetchone()
    if(data is not None):
        return render_template("index.html")
    else:
        guest=project( email=email, mobileNo=mobileNo, password=password)
        db.session.add(guest)
        db.session.commit()
        msg = Message(
            'Hello',
            sender='avinashkumaryadav0622@gmail.com',
            recipients=
            ['avinashkumaryadav.ece21@jecrc.ac.in'])
        msg.body = "This is the email body"
        msg.html=render_template("email.html",msg=email)
        mail.send(msg)
        return render_template("/signup.html")

@app.route("/login")
def login():
    email=request.args.get("email")
    password=request.args.get("pass")
    mycursor=mydb.cursor()
    sql="select * from project where email='"+email+"'"
    mycursor.execute(sql)
    data=mycursor.fetchone()
    print(data)
    if(data[0]==email):
        if(data[1]==password):
            return render_template("success.html")
        else:
            return render_template("index.html","error=password is not correct")
    else:
        return render_template("index.html",error="you are not registered user")



@app.route("/verifyEmail")
def verifyEmail():
    email = request.form.get("email")
    mycursor = mydb.cursor()
    sql ="update project set isverified=1 where email='" + email + "'"
    mycursor.execute(sql)
    mydb.commit()
    return "complete"


app.run()
