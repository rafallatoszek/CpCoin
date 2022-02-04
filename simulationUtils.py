from transaction import Transaction
from typing import List
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from blockChain import Blockchain
from user import User
from coin import Coin

def get_signed_transaction(transaction: Transaction, private_key):
    transaction_data = transaction.generate_data()
    hash_object = SHA256.new(transaction_data)
    signature = pkcs1_15.new(private_key).sign(hash_object)
    transaction.set_signature(signature)
    return transaction

def initiate_users_with_blockchain(users: List[User]):
    private_key = RSA.generate(1024)
    public_key =  private_key.publickey().export_key()
    coins = [Coin(1, 1), Coin(2, 1), Coin(3, 1), Coin(4, 1), Coin(5, 1)]
    user_idx = 0
    initial_transactions = []
    for coin in coins:
        if (user_idx >= len(users)):
            user_idx = 0

        transaction = Transaction(public_key, users[user_idx].public_key, coin)
        transaction = get_signed_transaction(transaction, private_key)
        initial_transactions.append(transaction)
        user_idx += 1
    # Create blockchain
    blockchain = Blockchain(initial_transactions)
    for user in users:
        user.set_blockchain(blockchain)
    return users