import random
from sympy import isprime, mod_inverse

def generate_prime(bits):
    while True:
        num = random.getrandbits(bits)
        if isprime(num):
            return num

def generate_keys(bits):
    p = generate_prime(bits)
    q = generate_prime(bits)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    d = mod_inverse(e, phi)
    return (e, n), (d, n)

def encrypt(public_key, message):
    e, n = public_key
    return pow(message, e, n)

def decrypt(private_key, ciphertext):
    d, n = private_key
    return pow(ciphertext, d, n)

public_key, private_key = generate_keys(8)
message = 4200015
ciphertext = encrypt(public_key, message)
decrypted_message = decrypt(private_key, ciphertext)

print("Public Key:", public_key)
print("Private Key:", private_key)
print("Original Message:", message)
print("Ciphertext:", ciphertext)
print("Decrypted Message:", decrypted_message)
