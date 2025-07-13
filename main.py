import os
from flask import Flask, request, render_template_string, redirect, url_for, jsonify
from dotenv import load_dotenv

load_dotenv()

def get_env(key, default=None):
    return os.environ.get(key, default)

def get_env_int(key, default):
    try:
        return int(os.environ.get(key, default))
    except (TypeError, ValueError):
        return default

def get_env_set(key, default):
    val = os.environ.get(key)
    if val:
        return set(x.strip() for x in val.split(",") if x.strip())
    return default

app = Flask(__name__)

app.secret_key = get_env('SECRET_KEY', 'dev')
UPLOAD_FOLDER = get_env('UPLOAD_FOLDER', os.path.expanduser('~/uploads')) or os.path.expanduser('~/uploads')
ALLOWED_EXTENSIONS = get_env_set('ALLOWED_EXTENSIONS', {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4'})
MAX_FILE_SIZE = get_env_int('MAX_FILE_SIZE', 10 * 1024 * 1024)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

HTML_FORM = '''
<!doctype html>
<html lang="en">
<head>
    <title>File Uploader</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: 'Inter', Arial, sans-serif;
            margin: 0;
            padding: 0;
            background: #fff;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            background: #fff;
            border-radius: 14px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.07);
            padding: 36px 32px 28px 32px;
            max-width: 420px;
            width: 100%;
            margin: 40px 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            border: 1px solid #eee;
        }
        h1 {
            color: #111;
            margin-bottom: 18px;
            font-size: 2rem;
            font-weight: 400;
            letter-spacing: -1px;
        }
        form {
            margin-top: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 100%;
        }
        .drop-area {
            width: 100%;
            min-height: 130px;
            border: 1.5px dashed #ccc;
            border-radius: 8px;
            background: #fafafa;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            margin-bottom: 12px;
            transition: border-color 0.2s, background 0.2s;
            position: relative;
        }
        .drop-area.dragover {
            border-color: #111;
            background: #f0f0f0;
        }
        .drop-area img.upload-icon {
            width: 20px;
            height: 20px;
            margin-bottom: 10px;
            opacity: 0.7;
        }
        .drop-area-text {
            color: #888;
            font-size: 1rem;
            font-weight: 400;
            text-align: center;
            font-style: normal;
        }
        .allowed-formats {
            display: block;
            color: #bbb;
            font-size: 0.92rem;
            margin-top: 4px;
            text-align: center;
        }
        .max-size {
            position: absolute;
            right: 10px;
            bottom: 8px;
            color: #bbb;
            font-size: 0.6rem;
            font-style: normal;
        }
        .custom-file-input {
            display: none;
        }
        button[type="submit"] {
            background: #111;
            color: #fff;
            border: none;
            border-radius: 6px;
            padding: 12px 28px;
            cursor: pointer;
            font-size: 1rem;
            font-weight: 400;
            margin-top: 8px;
            transition: background 0.2s, color 0.2s;
        }
        button[type="submit"]:hover {
            background: #222;
        }
        .messages {
            margin-top: 18px;
            text-align: left;
            width: 100%;
        }
        .alert {
            padding: 13px 16px;
            margin-bottom: 13px;
            border-radius: 6px;
            display: flex;
            align-items: center;
            font-size: 15px;
            background: #f6f6f6;
            color: #222;
            border: 1px solid #e5e7eb;
        }
        .file-list {
            width: 100%;
            margin-top: 18px;
        }
        .file-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: #fafafa;
            border: 1px solid #eee;
            border-radius: 6px;
            padding: 8px 12px;
            margin-bottom: 8px;
            font-size: 1rem;
        }
        .file-info {
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            flex: 1;
            min-width: 0;
        }
        .file-name, .file-size {
            color: #111;
            font-weight: 400;
            font-size: 1rem;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .file-size {
            color: #888;
            font-size: 0.95rem;
            margin-left: 0;
            margin-top: 2px;
        }
        .remove-btn {
            background: none;
            border: none;
            color: #888;
            font-size: 1.3em;
            cursor: pointer;
            margin-left: 10px;
            transition: color 0.2s;
        }
        .remove-btn:hover {
            color: #111;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>File Uploader</h1>
        {% with messages = get_flashed_messages(with_categories=true) %}
          {% if messages %}
            <div class="messages">
              {% for category, message in messages %}
                <div class="alert {{ category }}">
                  {{ message }}
                </div>
              {% endfor %}
            </div>
          {% endif %}
        {% endwith %}
        <form id="upload-form" action="/upload" method="post" enctype="multipart/form-data">
            <div class="drop-area" id="drop-area">
                <img src="{{ url_for('static', filename='upload.png') }}" alt="Upload" class="upload-icon" />
                <div class="drop-area-text">Click or drag file to this area to upload</div>
                <span class="allowed-formats">*{{ allowed_exts }}</span>
                <span class="max-size">MAX: {{ max_size_str }}</span>
                <input id="file-input" type="file" name="files" class="custom-file-input" multiple>
            </div>
            <div class="file-list" id="file-list"></div>
            <button type="submit">Upload</button>
        </form>
    </div>
    <script>
        const dropArea = document.getElementById('drop-area');
        const fileInput = document.getElementById('file-input');
        const fileList = document.getElementById('file-list');
        const uploadForm = document.getElementById('upload-form');
        let selectedFiles = [];
        const MAX_FILE_SIZE = {{ max_file_size }};

        dropArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropArea.classList.add('dragover');
        });
        dropArea.addEventListener('dragleave', (e) => {
            e.preventDefault();
            dropArea.classList.remove('dragover');
        });
        dropArea.addEventListener('drop', (e) => {
            e.preventDefault();
            dropArea.classList.remove('dragover');
            addFiles(e.dataTransfer.files);
        });
        dropArea.addEventListener('click', () => fileInput.click());
        fileInput.addEventListener('change', () => {
            addFiles(fileInput.files);
        });

        function addFiles(fileListObj) {
            const newFiles = Array.from(fileListObj);
            let rejected = [];
            for (const file of newFiles) {
                if (file.size > MAX_FILE_SIZE) {
                    rejected.push(file.name);
                    continue;
                }
                if (!selectedFiles.some(f => f.name === file.name && f.size === file.size)) {
                    selectedFiles.push(file);
                }
            }
            if (rejected.length > 0) {
                alert('File(s) too large: ' + rejected.join(', '));
            }
            updateInputFiles();
            renderFileList();
        }

        function formatSize(size) {
            if (size < 1024) return size + ' B';
            if (size < 1024 * 1024) return (size / 1024).toFixed(1) + ' KB';
            return (size / (1024 * 1024)).toFixed(2) + ' MB';
        }

        function renderFileList() {
            fileList.innerHTML = '';
            selectedFiles.forEach((file, idx) => {
                const item = document.createElement('div');
                item.className = 'file-item';
                item.innerHTML = `<span class=\"file-info\"><span class=\"file-name\">${file.name}</span><span class=\"file-size\">${formatSize(file.size)}</span></span>
                    <button type=\"button\" class=\"remove-btn\" title=\"Remove\">&times;</button>`;
                item.querySelector('.remove-btn').onclick = () => {
                    selectedFiles.splice(idx, 1);
                    updateInputFiles();
                    renderFileList();
                };
                fileList.appendChild(item);
            });
        }

        function updateInputFiles() {
            const dt = new DataTransfer();
            selectedFiles.forEach(file => dt.items.add(file));
            fileInput.files = dt.files;
        }

        uploadForm.addEventListener('submit', function(e) {
            if (selectedFiles.length === 0) return;
            e.preventDefault();
            const formData = new FormData();
            selectedFiles.forEach(f => formData.append('files', f));
            fetch('/upload', {
                method: 'POST',
                body: formData
            }).then(async resp => {
                alert('Selected files successfully uploaded');
                selectedFiles = [];
                updateInputFiles();
                renderFileList();
                if (resp.redirected) {
                    window.location = resp.url;
                }
            });
        });
    </script>
</body>
</html>
'''

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_unique_filename(directory, filename):
    if not directory or not filename:
        return None
    name, ext = os.path.splitext(filename)
    candidate = filename
    count = 1
    while os.path.exists(os.path.join(directory, candidate)):
        candidate = f"{name} ({count}){ext}"
        count += 1
    return candidate

@app.route('/')
def upload_form():
    allowed_exts = ', '.join(sorted(ALLOWED_EXTENSIONS))
    def format_max_size(size):
        if size < 1024:
            return f"{size} B"
        if size < 1024 * 1024:
            return f"{size // 1024} KB"
        return f"{size // (1024 * 1024)} MB"
    max_size_str = format_max_size(MAX_FILE_SIZE)
    return render_template_string(HTML_FORM, allowed_exts=allowed_exts, max_size_str=max_size_str, max_file_size=MAX_FILE_SIZE)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files' not in request.files:
        return redirect(url_for('upload_form'))
    files = request.files.getlist('files')
    if not files or all(not file.filename for file in files):
        return redirect(url_for('upload_form'))
    for file in files:
        if not file.filename:
            continue
        if not allowed_file(file.filename):
            continue
        if file.content_length is not None and file.content_length > MAX_FILE_SIZE:
            continue
        save_name = get_unique_filename(UPLOAD_FOLDER, file.filename)
        if not save_name:
            continue
        try:
            file.save(os.path.join(UPLOAD_FOLDER, save_name))
        except Exception:
            pass
    return redirect(url_for('upload_form'))

@app.route('/uploaded_files')
def uploaded_files():
    files = []
    if not UPLOAD_FOLDER:
        return jsonify(files)
    for fname in os.listdir(UPLOAD_FOLDER):
        fpath = os.path.join(UPLOAD_FOLDER, fname)
        if os.path.isfile(fpath):
            files.append({'name': fname, 'size': os.path.getsize(fpath)})
    return jsonify(files)

@app.route('/delete_file', methods=['POST'])
def delete_file():
    name = request.args.get('name')
    if not name or not UPLOAD_FOLDER:
        return '', 400
    fpath = os.path.join(UPLOAD_FOLDER, name)
    if os.path.exists(fpath):
        os.remove(fpath)
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)