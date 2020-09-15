from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import sys, os


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['inputFile']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save("uploads\\image.png")
        os.kill(os.getpid(), 9)
        #sys.exit(1)


if __name__ == '__main__':
    app.run(host= '0.0.0.0')
