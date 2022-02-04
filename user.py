import random
from typing import List
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA
from blockChain import Blockchain
from coin import Coin
from transaction import Transaction

class User:

    def __init__(self, username: str):
        self.username = username
        self.__private_key = RSA.generate(1024)
        self.public_key = self.__private_key.publickey().export_key()
        self.pending_transactions = []
       
    def get_blockchain(self):
        return self.__blockchain
        
    def set_blockchain(self, block_chain: Blockchain):
        self.__blockchain = block_chain
    
    def sign(self, transaction: Transaction):
        transaction_data = transaction.generate_data()
        hash_object = SHA256.new(transaction_data)
        signature = pkcs1_15.new(self.__private_key).sign(hash_object)
        transaction.set_signature(signature)
        return transaction

    def get_public_key(self):
        return str(self.public_key)

    def set_current_hash(self, hash: str):
        self.current_hash = hash

    def validate_blockchain_last_hash(self, last_hash):
        return self.current_hash == last_hash

    def create_transaction(self, sender: "User", recipient: "User", coin_id: int):
        coin = self.get_coin(sender.get_public_key(), coin_id)
        if coin == None:
            return False
        transaction = Transaction(sender.public_key, recipient.public_key, coin)
        return sender.sign(transaction)
        
    def get_coin(self, sender_pk: str, coin_id: int):
        user_coins = self.user_wallet_check(sender_pk)
        transaction_coin = None
        for i in range(0, len(user_coins)):
            if coin_id == user_coins[i].coin_id:
                transaction_coin = user_coins[i]
        return transaction_coin


    def user_wallet_check(self, user_pk: str):
        return self.__blockchain.user_wallet_check(user_pk)

    def broadcast_new_transaction(self, recipient: "User", coin_id: int, receivers: List["User"]):
        sender = self
        new_transaction = self.create_transaction(sender, recipient, coin_id)
        self.pending_transactions.append(new_transaction)

        for receiver in receivers:
            broadcasting_successful = random.uniform(0, 1) <= 0.9
            if not broadcasting_successful and receiver.public_key != self.public_key:
                print(f'Broadcasting to {receiver.username} randomly failed. Sender: {sender.username}')
            if broadcasting_successful and receiver.public_key != self.public_key:
                receiver.pending_transactions.append(new_transaction)

    def __receive_award(self):
        award_transaction = Transaction(self.public_key, self.public_key, Coin(6,1))
        award_transaction = self.sign(award_transaction)
        self.pending_transactions.append(award_transaction)

    def mine(self):
        print(self.username + " mines")
        self.__receive_award()
        self.__blockchain.append_blockchain(self.pending_transactions)
  
    def get_last_block_hash(self):
        return self.__blockchain.last_block.hash

    def validate_coins(self):
        for transaction in self.__blockchain.first_block.transactions:
            if not self.validate_signature(self.public_key, transaction.signature, transaction.generate_data()):
                return False
        
        return True

    def validate_transactions(self):
        for block in self.__blockchain.get_chain:
            for transaction in block.transactions:
                if not self.validate_signature(transaction.sender_pk, transaction.signature, transaction.generate_data()):
                    return False
        
        return True

    def validate_signature(self, public_key: bytes, signature: bytes, transaction_data: bytes):
        public_key_object = RSA.import_key(public_key)
        transaction_hash = SHA256.new(transaction_data)
        try:
            pkcs1_15.new(public_key_object).verify(transaction_hash, signature)
        except ValueError:
             return False
   
        return True

    def validate_blockchain(self):
        return self.__blockchain.validate_chain(self.__blockchain.get_chain)
    
    def validate_all(self):
        return self.validate_coins() and self.validate_transactions() and self.validate_blockchain()
    
   
