import os
import datetime
import subprocess
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(_name_)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]iasdfffsd/'

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'])



def CreateNewDir():
    print ("I am being called")
    global UPLOAD_FOLDER
    print (UPLOAD_FOLDER)
    UPLOAD_FOLDER = UPLOAD_FOLDER+datetime.datetime.now().strftime("%d%m%y%H")
    cmd="mkdir -p %s && ls -lrt %s"%(UPLOAD_FOLDER,UPLOAD_FOLDER)
    output = subprocess.Popen([cmd], shell=True,  stdout = subprocess.PIPE).communicate()[0]

    if "total 0" in output:
        print ("Success: Created Directory %s"%UPLOAD_FOLDER) 
    else:
        print ("Failure: Failed to Create a Directory (or) Directory already Exists",UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            UPLOAD_FOLDER = './upload_dir/'
            CreateNewDir()
            global UPLOAD_FOLDER
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@app.route('/uploaded', methods=['GET', 'POST'])
def uploaded_file():
	return '''
	<!doctype html>
	<title>Uploaded the file</title>
	<h1> File has been Successfully Uploaded </h1>
	'''

if _name_ == '_main_':
      app.secret_key = 'super secret key'
      app.config['SESSION_TYPE'] = 'filesystem'
      sess.init_app(app)
      app.debug = True
      app.run()