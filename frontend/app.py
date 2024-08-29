from flask import Flask, render_template, request, session
import random
from datetime import datetime
import time
import json
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.backends import default_backend

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def generate_data():
    temperature = round(random.uniform(20, 40))
    humidity = round(random.uniform(0, 10))
    return {
        'Temperature': temperature,
        'Humidity': humidity,
        'Time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

def generate_json(data_freq, interval):
    data = []
    for _ in range(data_freq):
        data_generated = generate_data()
        data.append(data_generated)
        time.sleep(interval)
    return data

def encrypt_data(key, data):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    json_data = json.dumps(data).encode('utf-8')
    encrypted_data = encryptor.update(json_data) + encryptor.finalize()
    return encrypted_data, iv

def generate_key(password):
    salt = os.urandom(16)
    kdf = Scrypt(
        salt=salt,
        length=32,
        n=2**14,
        r=8,
        p=1,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())
    return key, salt

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/post_data', methods=['POST'])
def post_data():
    frequency = int(request.form['frequency'])
    interval = int(request.form['interval'])
    password = request.form['password']
    data = generate_json(frequency, interval)
    session['data'] = data
    session['password'] = password
    return render_template('index.html', message="Data generated and stored in session.")

@app.route('/encrypt', methods=['POST'])
def encrypt():
    password = session.get('password')
    key, salt = generate_key(password)
    data = session.get('data')
    if data:
        encrypted_data, iv = encrypt_data(key, data)
        session['encrypted_data'] = {
            'encrypted_data': encrypted_data.hex(),
            'iv': iv.hex(),
            'salt': salt.hex()
        }
        return render_template('index.html', data=json.dumps(session['encrypted_data'], indent=4), message="Data encrypted and stored in session.")
    else:
        return render_template('index.html', data="No data available to encrypt.", message="No data available to encrypt.")

def decrypt_data(key, iv, encrypted_data):
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
    json_data = json.loads(decrypted_data)
    return json_data

@app.route('/decrypt', methods=['POST'])
def decrypt():
    password = request.form['password']
    encrypted_session_data = session.get('encrypted_data')
    if encrypted_session_data:
        encrypted_data = bytes.fromhex(encrypted_session_data['encrypted_data'])
        iv = bytes.fromhex(encrypted_session_data['iv'])
        salt = bytes.fromhex(encrypted_session_data['salt'])
        kdf = Scrypt(
            salt=salt,
            length=32,
            n=2**14,
            r=8,
            p=1,
            backend=default_backend()
        )
        key = kdf.derive(password.encode())
        try:
            decrypted_data = decrypt_data(key, iv, encrypted_data)
            return render_template('index.html', data=json.dumps(decrypted_data, indent=4), message="Data decrypted successfully.")
        except Exception as e:
            return render_template('index.html', data="Failed to decrypt data. Incorrect password.", message=str(e))
    else:
        return render_template('index.html', data="No encrypted data available to decrypt.", message="No encrypted data available to decrypt.")

if __name__ == '__main__':
    app.run(debug=True)
