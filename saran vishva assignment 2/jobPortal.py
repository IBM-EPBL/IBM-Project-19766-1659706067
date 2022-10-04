from crypt import methods
from flask import Flask,render_template,redirect,request
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

#configuration of Mysql Db

db = yaml.full_load(open('database.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route("/Home")
def home():
    return render_template("home.html")

@app.route("/Register")
def register():
    return render_template("register.html")

@app.route("/Register/user",methods=['GET','POST'])
def registerUser():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        mobile = request.form['mobile']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO USERS(name , email,password, mobile) VALUES(%s , %s, %s, %s)",(name,email,password,mobile))
        cur.connection.commit()
        cur.close()
        msg = 'registered Successfully'
        return render_template("login.html",msg = msg)
    else:
        return render_template("register.html")

@app.route("/Login",methods=["GET","POST"])
def login():
    return render_template("/login.html")

@app.route("/Login/user",methods=["GET","POST"])
def loginUser():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['psw']
        cur = mysql.connection.cursor()
        validUser = cur.execute("select * from USERS WHERE EMAIL = %s AND PASSWORD = %s",(email,password))
        cur.close()
        if validUser:
            msg = 'Login Sucessfully'
            return redirect('/Jobs')
        else:
            msg = 'Username or Password is wrong'
            return render_template('login.html',msg = msg)
        
@app.route("/Jobs")
def jobs():
    return render_template("jobs.html")

@app.route("/Jobs/Apply")
def applyJob():
    return render_template("apply.html")

@app.route("/Jobs/Apply/user",methods = ['GET','POST'])
def applyUser():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        mobile = request.form['mobile']
        skills = request.form['skills']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO jobApplications(name , email, mobile, skills) VALUES(%s , %s, %s, %s)",(name,email,mobile,skills))
        cur.connection.commit()
        cur.close()
        msg = 'Applied Successfully'
        return redirect("/Jobs")
    else:
        return render_template("apply.html")

if __name__ == "__main__":
    app.run(debug = True)