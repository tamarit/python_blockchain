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

transactions = []

def display_transactions(): 
    for transaction in transactions:
        display_transaction(transaction)
        print ('-'*14)

if __name__ == '__main__':
    # # Test Client
    # Dinesh = Client()
    # print(Dinesh.identity)
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
    # Test Multiple Transactions
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
 
    display_transactions()