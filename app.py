from flask import Flask, request
import os, time
from utils.encrypt import encrypt_file, decrypt_file
from flask import render_template
import json
import csv
import sys
import os


sys.path.append(os.path.dirname(os.path.abspath(__file__)))

DB_FILE = "database.csv"

def load_db():
    data = {}
    try:
        with open(DB_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data[row['filename']] = {
                    "expiry": float(row['expiry'])
                }
    except:
        pass
    return data

def save_db(data):
    with open(DB_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["filename", "expiry"])
        for filename, meta in data.items():
            writer.writerow([filename, meta["expiry"]])

DB_FILE = "database.json"

def load_db():
    with open(DB_FILE, 'r') as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)

app = Flask(__name__)
UPLOAD_FOLDER = "files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

file_db = {}



@app.route('/')
def home():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    expiry = int(request.form['expiry'])

    data = file.read()
    encrypted = encrypt_file(data)

    path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(path, 'wb') as f:
        f.write(encrypted)

    db = load_db()
    db[file.filename] = {
        "expiry": time.time() + expiry
    }
    save_db(db)

    return "File uploaded securely"

@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    db = load_db()

    if filename not in db:
        return "File not found"

    if time.time() > db[filename]["expiry"]:
        os.remove(f"files/{filename}")
        del db[filename]
        save_db(db)
        return "File expired and deleted"

    with open(f"files/{filename}", 'rb') as f:
        encrypted = f.read()

    decrypted = decrypt_file(encrypted)

    os.remove(f"files/{filename}")
    del db[filename]
    save_db(db)

    return decrypted
if __name__ == '__main__':
    app.run(debug=True)