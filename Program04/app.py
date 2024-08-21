import time
import hashlib

class Block:
    def __init__(self,index,previous_hash,timestamp,data,hash):
        self.index=index
        self.previous_hash=previous_hash
        self.timestamp=timestamp
        self.data=data
        self.hash=hash
    
def display_blockchain(blockchain):
    for block in blockchain:
        print("index:",block.index)
        print("previous hash:",block.previous_hash)
        print("timestamp:",block.timestamp)
        print("data:",block.data)
        print("hash:",block.hash)
        print("\n")

def calculate_hash(index, previous_hash, timestamp, data):
    value = f"{index}{previous_hash}{timestamp}{data}"
    hash_object = hashlib.sha256()
    hash_object.update(value.encode('utf-8'))
    hash_code = hash_object.hexdigest()
    return hash_code

def create_genesis_block():
    timestamp=int(time.time())
    return Block(0,"0",timestamp,"Genesis Block",calculate_hash(0,"0",timestamp,"Genesis Block"))

def create_new_block(previous_block,data):
    index=previous_block.index+1
    timestamp=int(time.time())
    hash=calculate_hash(index,previous_block.hash,timestamp,data)
    return Block(index,previous_block.hash,timestamp,data,hash)



blockchain=[create_genesis_block()]
print("genesis block added successfully")

print("creating more blocks")

blockchain.append(create_new_block(blockchain[-1],"BLOCK 1 DATA"))
blockchain.append(create_new_block(blockchain[-1],"BLOCK 2 DATA"))
blockchain.append(create_new_block(blockchain[-1],"BLOCK 3 DATA"))
blockchain.append(create_new_block(blockchain[-1],"BLOCK 4 DATA"))
blockchain.append(create_new_block(blockchain[-1],"BLOCK 5 DATA"))
blockchain.append(create_new_block(blockchain[-1],"BLOCK 6 DATA"))

print("genesis block and other blocks added")
display_blockchain(blockchain)

