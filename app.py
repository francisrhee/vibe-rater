import flask
import sys
import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, session
from werkzeug.utils import secure_filename
from predict import getPrediction


app = Flask(__name__, template_folder='templates')
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = "uploads/"
app.debug=True

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        print("get", file=sys.stderr)
        return(flask.render_template('main.html'))
    if request.method == 'POST':
        print("post", file=sys.stderr)
        if 'file' not in request.files:
            print("No file part", file=sys.stderr)
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print("No selected file", file=sys.stderr)
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(url_for('results', filename=filename), file=sys.stderr)
            return redirect(url_for('results', filename=filename))

@app.route('/results/<filename>')
def results(filename):
    print("test ", file=sys.stderr)
    result = getPrediction(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    print("file", result, file=sys.stderr)
    return result

    # TODO: Find out how to 1. pass in image rather than saving 2. use this image in tensorflow 
    #send_from_directory(app.config['UPLOAD_FOLDER'], filename) # prints image on screen
    # if request.method == 'POST':
    #     # TODO:
    #     # 2. Figure out how to load and use model to generate prediction output
    #     # 3. Test out this prediction on postman
    #     # 4. Currently we're saving the file on the server then using it, but we would need to delete it which takes time - can we just hold onto it temporarily?

    #     # tensorflow logic
    #     # get image from request (test out using print image name?), pass into model
    #     # can test out this endpoint separately from main through postman?
    #     pass 




if __name__ == '__main__':
    print("test22222", file=sys.stderr)
    app.run(debug=True)
