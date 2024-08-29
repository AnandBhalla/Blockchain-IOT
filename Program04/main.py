import time
import hashlib

input_file = 'data.txt'
programmer_output_file = 'programmer_file.txt'
user_output_file='user_output_file.txt'

def readFile(input_file):
    with open(input_file, 'r') as file:
        content = file.read()
    return content

def writeFile(programmer_output_file, blockchain):
    blockchain_data = ""
    user_data=""
    for block in blockchain:
        blockchain_data += f"index: {block.index}\n"
        blockchain_data += f"previous hash: {block.previous_hash}\n"
        blockchain_data += f"timestamp: {block.timestamp}\n"
        blockchain_data += f"data: {block.data}\n"
        blockchain_data += f"hash: {block.hash}\n"
        blockchain_data += "\n"
        user_data+=block.hash
    with open(programmer_output_file, 'w') as file:
        file.write(blockchain_data)
    with open(user_output_file, 'w') as file:
        file.write(user_data)

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

def calculate_hash(index, previous_hash, timestamp, data):
    value = f"{index}{previous_hash}{timestamp}{data}"
    hash_object = hashlib.sha256()
    hash_object.update(value.encode('utf-8'))
    hash_code = hash_object.hexdigest()
    return hash_code

def create_genesis_block():
    timestamp = int(time.time())
    return Block(0, "0", timestamp, "Genesis Block", calculate_hash(0, "0", timestamp, "Genesis Block"))

def create_new_block(previous_block, data):
    index = previous_block.index + 1
    timestamp = int(time.time())
    hash = calculate_hash(index, previous_block.hash, timestamp, data)
    return Block(index, previous_block.hash, timestamp, data, hash)

blockchain = [create_genesis_block()]

data = readFile(input_file)

words = data.split()

for word in words:
    new_block = create_new_block(blockchain[-1], word)
    blockchain.append(new_block)

writeFile(programmer_output_file, blockchain)

print("Genesis block and other blocks added")
