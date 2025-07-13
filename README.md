<a id="readme-top"></a>

# File Uploader

This app is a web-based tool built with Flask that provides a clean, drag-and-drop interface for uploading multiple files to a server over a local network with configurable file type restrictions and size limits.

<p align="left">
   <img width="600" alt="image" src="https://github.com/user-attachments/assets/ad18c1bd-fc30-4360-94b4-fafac27c3382"/>
</p>

## Description

File Uploader creates a user-friendly file upload service that individuals can purpose it for:

- Cross-Device File Transfer: moving files between different devices
- Team Collaboration: rapidly sharing files within teams to the manager rather than through email
- Student Submission: collecting assignments, projects or multimedia submissions for teachers

The web application allows users to either click to select files or drag and drop them directly onto the upload area. The selected files are then displayed in a formatted list, with options to remove any one from the queue. File types and file size limits are in place and are validated to allow or disallow the upload. Users can click upload, rapidly transferring all selected files to the host's designated computer or server folder. Duplication handling is in place which automatically renames files if they already exist in the upload directory rather than overwriting. The responsive design features a clean, modern UI that works across different screen sizes: phone, tablet or computer.

## Built With

- [Python 3.13](https://www.python.org/): Programming language for backend logic and file handling
- [Flask 3.1](https://flask.palletsprojects.com/en/stable/): Lightweight framework for creating the REST API endpoints and serving the web interface
- [python-dotenv 0.9](https://pypi.org/project/python-dotenv/): Environment variable management for secure configuration of upload settings and file restrictions

## Quick Start

### Prerequisites

- OS
- Python 3.13 or higher
- Internet Connection
- Terminal or CLI Access

### Installation

To install the File Uploader, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/jusL98/file-uploader.git
   cd file-uploader
   ```

2. Ensure that you have python running on your system.

3. Create and activate a virtual environment:

   - On Windows:

   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```

   - On macOS and Linux:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

4. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Copy and edit the .env file:

   ```bash
   cp .env.example .env
   ```

### Setup

6. Open the .env file:

   - On Windows:

   ```bash
   notepad .env
   ```

   - On macOS or Linux

   ```bash
   open .env
   ```

7. Edit the environment variables to your liking:

   | Variable           | Description                            | Example                      |
   | ------------------ | -------------------------------------- | ---------------------------- |
   | SECRET_KEY         | Flask secret key (use a random string) | `SECRET_KEY=dev`             |
   | UPLOAD_FOLDER      | Where to save uploaded files           | `UPLOAD_FOLDER=uploads`      |
   | ALLOWED_EXTENSIONS | Allowed file types                     | `ALLOWED_EXTENSIONS=txt,png` |
   | MAX_FILE_SIZE      | Max file size in bytes                 | `MAX_FILE_SIZE=10485760`     |

   Don't add spaces around the = sign in the variables.
   Don't wrap values in quotes unless they contain spaces.
   ALLOWED_EXTENSIONS are comma-separated, no spaces.
   Common MAX_FILE_SIZEs: 10MB: 10485760, 25MB: 26214400, 50MB: 52428800, 100MB: 104857600

   ex. `.env`

   ```
   SECRET_KEY=EAedoL2IiWeMhsS4klBDB3rZzPzMGUCC
   UPLOAD_FOLDER=C:\Users\YourName\Documents\uploads
   ALLOWED_EXTENSIONS=txt,pdf,png,jpg,jpeg,gif,mp4,doc,docx,xls,xlsx,zip
   MAX_FILE_SIZE=10485760
   ```

### Run

8. Start the Flask application:
   ```bash
   python main.py
   ```
9. Access the web interface:

   - Open your web browser and navigate to: `http://localhost:5000`
   - For network access from other devices: `http://YOUR_IP_ADDRESS:5000`

10. Use File Uploader, allowing other devices to upload files to the host computer!

11. Stop the application:
   - Press `Ctrl+C` or `Cmd+C` in the host terminal to stop the server.
   - Or simply close terminal.

## Usage

1. **Access the web interface** at `http://localhost:5000` or `http://YOUR_IP_ADDRESS:5000` from other devices
2. **Upload files** using drag-and-drop or click to select
3. **Monitor uploads** through the web interface progress indicators
4. **Find uploaded files** in the host computer's configured upload directory
5. **Check file validation** (only allowed file types and sizes will be accepted)

## Contributing

1. Fork & branch off main.
2. Make your changes.
3. PRs welcome!

## Project Structure

```
├── file-uploader/
│   ├── static/
│   │   └── upload.png                 // upload icon image file
│   │
│   ├── .env                           // contains environment variables for configuration
│   ├── .env.example                   // sample .env file
│   ├── requirements.txt               // list of required dependencies for easy installation
│   └── main.py                        // contains methods that controls the Connect 4 board
```

## Acknowledgements
This project was created to learn the lightweight Flask framework for Python and to make file transfers from device to device more seamless for myself.

## License
This project is licensed under the [MIT](LICENSE.txt) License. See LICENSE.txt for more information.

<br>

---

<br>
Thank you!

<p align="left">
  <a href="mailto:justin.matthew.lee.18@gmail.com">
    <img src="https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white"/>
  </a>
  <a href="https://www.linkedin.com/in/justin-matthew-lee/">
    <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"/>
  </a>
    <a href="https://github.com/jusl98">
    <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"/>
  </a>
</p>

<p align="right">(<a href="#readme-top">BACK TO TOP</a>)</p>
