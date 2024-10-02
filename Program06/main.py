import random
import math

def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

def generate_prime():
    while True:
        num = random.randint(100, 1000)
        if is_prime(num):
            return num

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def mod_inv(a, m):
    if gcd(a, m) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m

def generate_keys():
    p = generate_prime()
    q = generate_prime()
    n = p * q
    phi = (p - 1) * (q - 1)
    e = random.randint(2, phi - 1)
    while gcd(e, phi) != 1:
        e = random.randint(2, phi - 1)
    d = mod_inv(e, phi)
    public_key = (e, n)
    private_key = (d, n)
    return public_key, private_key

def encrypt(message, public_key):
    e, n = public_key
    encrypted_message = [pow(ord(char), e, n) for char in message]
    return encrypted_message

def decrypt(encrypted_message, private_key):
    d, n = private_key
    decrypted_message = [chr(pow(char, d, n)) for char in encrypted_message]
    return ''.join(decrypted_message)

public_key, private_key = generate_keys()
print("Public key:", public_key)
print("Private key:", private_key)

message = input("Enter your message: ")
encrypted_message = encrypt(message, public_key)
print("Encrypted message:", ''.join(map(str, encrypted_message)))

decrypted_message = decrypt(encrypted_message, private_key)
print("Decrypted message:", decrypted_message)
