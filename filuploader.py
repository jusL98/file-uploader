from flask import Flask, request, render_template_string, flash, redirect, url_for
import os
import logging

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flashing messages
UPLOAD_FOLDER = "C:/Users/HP/Downloads"  # Change this to your desired folder
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}  # Allowed file extensions
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Configure logging
logging.basicConfig(level=logging.INFO)

HTML_FORM = '''
<!doctype html>
<html>
<head>
    <title>File Uploader</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #f0f2f5;
        }
        .container {
            text-align: center;
            background: #ffffff;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 6px 10px rgba(0, 0, 0, 0.1);
            width: 90%;
            max-width: 500px;
        }
        h1 {
            color: #333;
            margin-bottom: 20px;
        }
        form {
            margin-top: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .custom-file-input {
            display: none;
        }
        .custom-file-label {
            display: inline-block;
            background-color: #007BFF;
            color: white;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            margin-bottom: 10px;
        }
        .custom-file-label:hover {
            background-color: #0056b3;
        }
        button {
            background-color: #28a745;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #218838;
        }
        .messages {
            margin-top: 20px;
            text-align: left;
        }
        .alert {
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 4px;
            display: flex;
            align-items: center;
            font-size: 14px;
        }
        .alert.success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .alert.error {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .alert .icon {
            margin-right: 10px;
            font-size: 18px;
        }
        .alert.success .icon {
            color: #28a745;
        }
        .alert.error .icon {
            color: #dc3545;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Upload Files</h1>
        {% with messages = get_flashed_messages(with_categories=true) %}
          {% if messages %}
            <div class="messages">
              {% for category, message in messages %}
                <div class="alert {{ category }}">
                  <span class="icon">{{ '✔' if category == 'success' else '✖' }}</span>
                  {{ message }}
                </div>
              {% endfor %}
            </div>
          {% endif %}
        {% endwith %}
        <form action="/upload" method="post" enctype="multipart/form-data">
            <label for="file-input" class="custom-file-label">Choose Files</label>
            <input id="file-input" type="file" name="files" class="custom-file-input" multiple required>
            <button type="submit">Upload</button>
        </form>
    </div>
</body>
</html>
'''

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
    return render_template_string(HTML_FORM)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files' not in request.files:
        flash("No file part", "error")
        return redirect(url_for('upload_form'))

    files = request.files.getlist('files')

    if not files or all(file.filename == '' for file in files):
        flash("No selected files", "error")
        return redirect(url_for('upload_form'))

    for file in files:
        if file.filename == '':
            continue  # Skip empty file fields

        if not allowed_file(file.filename):
            flash(f"File type not allowed: {file.filename}", "error")
            continue

        try:
            file.save(os.path.join(UPLOAD_FOLDER, file.filename))
            flash(f"File uploaded successfully: {file.filename}", "success")
            logging.info(f"File uploaded: {file.filename}")
        except Exception as e:
            flash(f"File upload failed for {file.filename}: {str(e)}", "error")
            logging.error(f"File upload failed for {file.filename}: {str(e)}")

    return redirect(url_for('upload_form'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)