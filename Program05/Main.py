import hashlib
import time
from tqdm import tqdm

def hash_pair(hash1, hash2):
    return hashlib.sha256((hash1 + hash2).encode('utf-8')).hexdigest()

def merkle_tree():
    transactions = create_transactions()
    hashed_transactions = create_hash_list(transactions)
    
    merkle_root = build_merkle_root(hashed_transactions)
    
    print("Merkle Root:", merkle_root)
    
    flag = True
    for t in transactions:
        if not verification(t, merkle_root, hashed_transactions):
            flag = False
            break

    if flag:
        print("All transactions verified ✅")
    else:
        print("Verification failed ❌")

def create_transactions():
    transactions = []
    interval = 2
    frequency = 10
    for i in tqdm(range(frequency), desc="Creating transactions"):
        t = time.time()
        transactions.append(t)
        time.sleep(interval)
    return transactions

def create_hash_list(transactions):
    hashed_transactions = []
    for t in transactions:
        t = hashlib.sha256(str(t).encode('utf-8')).hexdigest()
        hashed_transactions.append(t)
    return hashed_transactions

def build_merkle_root(transactions):
    current_level = transactions
    while len(current_level) > 1:
        next_level = []
        for i in range(0, len(current_level), 2):
            if i + 1 < len(current_level):
                combined_hash = hash_pair(current_level[i], current_level[i + 1])
            else:
                combined_hash = hash_pair(current_level[i], current_level[i])
            next_level.append(combined_hash)
        current_level = next_level
    return current_level[0]

def verification(transaction, root, transactions):
    current_hash = hashlib.sha256(str(transaction).encode('utf-8')).hexdigest()
    current_level = transactions
    
    while len(current_level) > 1:
        next_level = []
        for i in range(0, len(current_level), 2):
            if i + 1 < len(current_level):
                if current_level[i] == current_hash or current_level[i + 1] == current_hash:
                    combined_hash = hash_pair(current_level[i], current_level[i + 1])
                    current_hash = combined_hash
            else:
                if current_level[i] == current_hash:
                    combined_hash = hash_pair(current_level[i], current_level[i])
                    current_hash = combined_hash
            next_level.append(hash_pair(current_level[i], current_level[i + 1]) if i + 1 < len(current_level) else hash_pair(current_level[i], current_level[i]))
        current_level = next_level
    
    return current_hash == root

merkle_tree()
