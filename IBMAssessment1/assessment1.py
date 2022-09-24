from fileinput import filename
from flask import Flask,render_template,request,redirect
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

#initialising the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#this one represents the database configuration of table
class Upload(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)

#Register page
@app.route('/')
def registerPage():
    return render_template('assesment1.html')

#file uploading page
@app.route('/upload',methods=['GET','POST'])
def uploadfile():
    files = Upload.query.all()
    return render_template('files.html',files = files)

#uploading the file in db
@app.route('/uploader',methods=['GET','POST'])
def uploaderfile():   
    if request.method == 'POST':
        f=request.files['file']
        upload = Upload(filename = f.filename, data = f.read())#adding the file into to database
        
        try:
            db.session.add(upload)
            db.session.commit()
            return redirect('/upload')
        except:
            return "there is an issue to add the file"
    else:
        files = Upload.query.all()
        return render_template('files.html', files= files)

#deleting the file
@app.route('/delete/<int:id>')
def delete(id):
    deleteTask = Upload.query.get_or_404(id)
    
    try:
        db.session.delete(deleteTask)
        db.session.commit()
        return redirect('/upload')
    except:
        return "there is an issue in delete the element"

#updating the file
@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    file = Upload.query.get_or_404(id)
    if request.method == 'POST':
        f = request.files['file']
        file.filename = f.filename
        file.data = f.read()
        
        try:
            db.session.commit()
            return redirect('/upload')
        except:
            return "There is an error in uploading a file"
    else:
        return render_template('update.html',file = file)
        

# @app.before_first_request
# def create_tables():
#     db.create_all()

if __name__=='__main__':
    app.run(debug=True)