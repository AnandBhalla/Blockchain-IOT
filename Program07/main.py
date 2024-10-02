import hashlib
import os
from ecdsa import VerifyingKey, SigningKey, SECP256k1

def generate_key_pair():
    sk = SigningKey.from_secret_exponent(1, curve=SECP256k1)
    vk = sk.verifying_key
    return sk, vk

def encrypt(message, vk):
    encrypted_message = vk.to_string() + hashlib.sha256(message.encode()).digest()
    return encrypted_message

def decrypt(encrypted_message, sk):
    vk_string = encrypted_message[:64]
    vk = VerifyingKey.from_string(vk_string, curve=SECP256k1)
    message_hash = encrypted_message[64:]
    if hashlib.sha256(message.encode()).digest() == message_hash:
        return message
    else:
        return "Decryption failed"

sk, vk = generate_key_pair()
print("Private key:", sk.to_string().hex())
print("Public key:", vk.to_string().hex())

message = "Hello, World! 123 WELCOME"
print("Original message:", message)

encrypted_message = encrypt(message, vk)
print("Encrypted message:", encrypted_message.hex())

decrypted_message = decrypt(encrypted_message, sk)
print("Decrypted message:", decrypted_message)