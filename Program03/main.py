from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
import json

input_file = 'D:\\Blockchain-IOT\\Program01\\data.json'

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


admin_password = "admin123"
user_password = input("enter password:")

admin_key, admin_salt = generate_key(admin_password)
user_key, user_salt = generate_key(user_password)

def encrypt_data(key, data):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    json_data = json.dumps(data).encode('utf-8')
    encrypted_data = encryptor.update(json_data) + encryptor.finalize()
    return encrypted_data, iv

with open(input_file, 'r') as file:
        data=json.load(file)

admin_encrypted_data, admin_iv = encrypt_data(admin_key, data)
user_encrypted_data, user_iv = encrypt_data(user_key, data)


def decrypt_data(key, encrypted_data, iv):
    check=input("enter password:")
    if(check==user_password):
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
        json_data = json.loads(decrypted_data)
        return json_data 
    
    


admin_decrypted_data = decrypt_data(admin_key, admin_encrypted_data, admin_iv)
print(f"Admin Decrypted Data: {admin_decrypted_data}")


user_decrypted_data = decrypt_data(user_key, user_encrypted_data, user_iv)
print(f"User Decrypted Data: {user_decrypted_data}")


