# import libraries
import hashlib
import random
import string
import json
import binascii
import numpy as np
import pandas as pd
import pylab as pl
import logging
import datetime
import collections

# following imports are required by PKI
import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5


###########################################
# Classes
###########################################

class Client:

    def __init__(self):
        random = Crypto.Random.new().read 
        self._private_key = RSA.generate(1024, random) 
        self._public_key = self._private_key.publickey() 
        self._signer = PKCS1_v1_5.new(self._private_key)

    @property
    def identity(self):
        return binascii.hexlify(self._public_key.exportKey(format='DER')).decode('ascii')

class Transaction:

    def __init__(self, sender, recipient, value):
        self.sender = sender
        self.recipient = recipient
        self.value = value
        self.time = datetime.datetime.now()
    
    def to_dict(self):
        if self.sender == "Genesis":
            identity = "Genesis"
        else:
            identity = self.sender.identity
        return collections.OrderedDict({
            'sender': identity, 
            'recipient': self.recipient,
            'value': self.value,
            'time' : self.time
        })
    
    def sign_transaction(self):
        private_key = self.sender._private_key
        signer = PKCS1_v1_5.new(private_key)
        h = SHA.new(str(self.to_dict()).encode('utf8'))
        return binascii.hexlify(signer.sign(h)).decode('ascii')

class Block:

    def __init__(self):
        self.verified_transactions = []
        self.previous_block_hash = ""
        self.Nonce = ""

class BlockChain:

    def __init__(self):
        self.TPCoins = []

    def dump_blockchain (self):
        print(f"Number of blocks in the chain: {len(self)}" + str(len (self)))
        for x, block_temp in enumerate(self.TPCoins):
            print(f"block # {x}")
            for transaction in block_temp.verified_transactions:
                display_transaction(transaction)
                print ('-'*14)
            print ('='*37)

###########################################
# Global variables
###########################################

last_block_hash = ""
transactions = []
TPCoins = []
last_transaction_index = 0


###########################################
# Utility methods
###########################################

def print_with_separators(str_list):
    print(("\n" + "-"*5 + "\n").join(str_list))

def display_transaction(transaction): 
    transaction_dict = transaction.to_dict()
    print_with_separators([
        f"sender: {transaction_dict['sender']}",
        f"recipient: {transaction_dict['recipient']}",
        f"value: {transaction_dict['value']}",
        f"valtimeue: {transaction_dict['time']}",
    ])

def display_transactions(): 
    for transaction in transactions:
        display_transaction(transaction)
        print ('-'*14)

def dump_blockchain():
    print(f"Number of blocks in the chain: {len(TPCoins)}")
    for x, block_temp in enumerate(TPCoins):
        print(f"block # {x}")
        for transaction in block_temp.verified_transactions:
            display_transaction(transaction)
            print ('-'*14)
        print ('='*37)

def sha256(message):
    return hashlib.sha256(message.encode('ascii')).hexdigest()

def mine(message, difficulty=1):
    assert difficulty >= 1
    prefix = '1'*difficulty
    # for i in range(1000):
    for i in range(10000000):
        digest = sha256(str(hash(message)) + str(i))
        if digest.startswith(prefix):
            print(f"after {i} iterations found nonce: {digest}")
            return digest

if __name__ == '__main__':
    ###########################################
    # #??Test Client
    # Dinesh = Client()
    # print(Dinesh.identity)

    ###########################################
    # # Test Transaction
    # Dinesh = Client()
    # Ramesh = Client()
    # t = Transaction(
    #     Dinesh,
    #     Ramesh.identity,
    #     5.0
    # )
    # signature = t.sign_transaction()
    # print (signature)

    ###########################################
    # # Test Multiple Transactions
    Dinesh = Client()
    Ramesh = Client()
    Seema = Client()
    Vijay = Client()

    t1 = Transaction(
        Dinesh,
        Ramesh.identity,
        15.0 
    )
    t1.sign_transaction()
    transactions.append(t1)

    t2 = Transaction(
        Dinesh,
        Seema.identity,
        6.0
    )
    t2.sign_transaction()
    transactions.append(t2)

    t3 = Transaction(
        Ramesh,
        Vijay.identity,
        2.0 
    )
    t3.sign_transaction()
    transactions.append(t3)

    t4 = Transaction(
        Seema,
        Ramesh.identity,
        4.0
    )
    t4.sign_transaction()
    transactions.append(t4)

    t5 = Transaction(
        Vijay,
        Seema.identity,
        7.0
    )
    t5.sign_transaction()
    transactions.append(t5)

    t6 = Transaction(
        Ramesh,
        Seema.identity,
        3.0
    )
    t6.sign_transaction()
    transactions.append(t6)

    t7 = Transaction(
        Seema,
        Dinesh.identity,
        8.0
    )
    t7.sign_transaction()
    transactions.append(t7)

    t8 = Transaction(
        Seema,
        Ramesh.identity,
        1.0
    )
    t8.sign_transaction()
    transactions.append(t8)

    t9 = Transaction(
        Vijay,
        Dinesh.identity,
        5.0
    )
    t9.sign_transaction()
    transactions.append(t9)

    t10 = Transaction(
        Vijay,
        Ramesh.identity,
        3.0
    )
    t10.sign_transaction()
    transactions.append(t10)
 
    # display_transactions()

    ###########################################
    # # Test Block Creation & Visualization
    # Dinesh = Client()
    # t0 = Transaction(
    #     "Genesis",
    #     Dinesh.identity,
    #     500.0 
    # )
    # block0 = Block()

    # block0.previous_block_hash = None
    # Nonce = None

    # block0.verified_transactions.append(t0)

    # digest = hash(block0)
    # last_block_hash = digest
    # print(last_block_hash)

    # TPCoins.append(block0)
    
    # dump_blockchain()

    # ###########################################
    # # Mining test
    
    # mine("test message daa dasd asda sd", 4)

    ###########################################
    # Adding a block

    for _ in range(3):
        block = Block()
        for i in range(3):
            temp_transaction = transactions[last_transaction_index] 
            # validate transaction
            # if valid
            block.verified_transactions.append(temp_transaction)
            last_transaction_index += 1
            
        block.previous_block_hash = last_block_hash 
        block.Nonce = mine (block, 2)
        digest = hash (block)
        TPCoins.append (block)
        last_block_hash = digest

    dump_blockchain()





