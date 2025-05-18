from flask import Flask, render_template, request
import os
import time
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
RESULTS_FOLDER = 'static/results'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if 'cloth' not in request.files or 'model' not in request.files:
        return "Missing files", 400

    cloth_file = request.files['cloth']
    model_file = request.files['model']

    if cloth_file.filename == '' or model_file.filename == '':
        return "No selected file", 400

    if allowed_file(cloth_file.filename) and allowed_file(model_file.filename):
        cloth_filename = secure_filename(cloth_file.filename)
        model_filename = secure_filename(model_file.filename)

        cloth_path = os.path.join(app.config['UPLOAD_FOLDER'], cloth_filename)
        model_path = os.path.join(app.config['UPLOAD_FOLDER'], model_filename)

        cloth_file.save(cloth_path)
        model_file.save(model_path)

        # Create the combined output filename: modelname + clothname
        output_filename = f"{os.path.splitext(model_filename)[0]}{os.path.splitext(cloth_filename)[0]}.png"

        # Check if combined image exists in results folder
        output_path = os.path.join(app.config['RESULTS_FOLDER'], output_filename)
        if not os.path.exists(output_path):
            return f"Result image {output_filename} not found in results folder.", 404
        time.sleep(5)

        return render_template('result.html',
                               cloth_image=cloth_filename,
                               model_image=model_filename,
                               output_image=output_filename)
    else:
        return "Invalid file type", 400

if __name__ == '__main__':
    app.run(debug=True)
