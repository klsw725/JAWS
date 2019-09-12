import os
from flask import Flask, make_response, render_template, url_for, request, flash, redirect, jsonify
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'media'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__, static_folder='media')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=["POST", "GET"])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file'] or request.files['media']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify({
                "result": "success",
            })

    uploaded_files = os.listdir(app.config['UPLOAD_FOLDER'], )

    file_components = ["<a href='/media/{file_name}'>{file_name}</a>".format(file_name=uploaded_file) for uploaded_file in uploaded_files]
    return """
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    {file_components}
    """.format(file_components="<br>".join(file_components))

if __name__ == '__main__':
    app.run()

