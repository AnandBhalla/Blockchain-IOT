import time
import hashlib

input_file = 'Program04\data.txt'
programmer_output_file = 'programmer_file.txt'
user_output_file = 'user_output_file.txt'

def readFile(input_file):
    with open(input_file, 'r') as file:
        content = file.read()
    return content

def writeFile(programmer_output_file, user_output_file, blockchain):
    blockchain_data = []
    user_data = []
    for block in blockchain:
        blockchain_data.append(f"index: {block.index}\n"
                               f"previous hash: {block.previous_hash}\n"
                               f"timestamp: {block.timestamp}\n"
                               f"data: {block.data}\n"
                               f"hash: {block.hash}\n")
        user_data.append(block.hash)
    blockchain_data_str = "".join(blockchain_data)
    user_data_str = "".join(user_data)
    with open(programmer_output_file, 'w') as prog_file:
        prog_file.write(blockchain_data_str)
    with open(user_output_file, 'w') as user_file:
        user_file.write(user_data_str)


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
    return hash_object.hexdigest()

def create_genesis_block():
    timestamp = int(time.time())
    return Block(0, "0", timestamp, "Genesis Block", calculate_hash(0, "0", timestamp, "Genesis Block"))

def create_new_block(previous_block, data):
    index = previous_block.index + 1
    timestamp = int(time.time())
    new_hash = calculate_hash(index, previous_block.hash, timestamp, data)
    return Block(index, previous_block.hash, timestamp, data, new_hash)

blockchain = [create_genesis_block()]

data = readFile(input_file)
words = data.split()

for word in words:
    new_block = create_new_block(blockchain[-1], word)
    blockchain.append(new_block)

writeFile(programmer_output_file,user_output_file, blockchain)

print("Genesis block and other blocks added.")
