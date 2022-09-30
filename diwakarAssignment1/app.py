from crypt import methods
from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///registration.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))
    email = db.Column(db.String(50))
    gender = db.Column(db.String(50))
    state = db.Column(db.String(50))
    
@app.route('/')
def registerUser():
    return render_template("register.html")

@app.route('/register',methods=['GET','POST'])
def registerData():
    if request.method == 'POST':
        userName = request.form['name']
        email = request.form['email']
        password = request.form['password']
        gender = request.form['status']
        state = request.form['state']
        
        userDetails = User(name = userName,email = email,password = password,gender = gender,state = state)
    
        try:
            db.session.add(userDetails)
            db.session.commit()
            return redirect('/users')
        except:
            return "there is an error to register the User"
    else:
        users = User.query.all()
        return render_template('userdetails.html',users = users)

@app.route('/users',methods=['GET' , 'POST'])
def getUsers():
    users = User.query.all()
    return render_template('userdetails.html',users = users)


@app.route('/updateUser/<int:id>',methods=['GET','POST'])
def update(id):
    user= User.query.get_or_404(id)
    if request.method == 'POST':
        name = request.form['userName']
        email = request.form['emailId']
        password = request.form['password']
        gender = request.form['status']
        state = request.form['state']
        
        
        user.name = name
        user.email = email
        user.password = password
        user.gender = gender
        user.state = state
        
        try:
            db.session.commit()
            return redirect('/upload')
        except:
            return "There is an error in uploading a file"
    else:
        return render_template('updateuser.html',user = user)
    
@app.route('/delete/<int:id>')
def delete(id):
    deleteuser = User.query.get_or_404(id)
    
    try:
        db.session.delete(deleteuser)
        db.session.commit()
        return redirect('/users')
    except:
        return "there is an issue in delete the element"


if __name__=='__main__':
    app.run(debug=True)
