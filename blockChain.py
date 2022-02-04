import hashlib
import random
from typing import List
from block import Block
from transaction import Transaction

class Blockchain:

    @property
    def last_block(self):
        return self.__chain[-1]

    @property
    def first_block(self):
        return self.__chain[0]

    @property
    def get_chain(self):
        return self.__chain

    def __init__(self, initial_transactions: List[Transaction]):
        self.__chain = []
        self.__difficulty = 55
        self.create_genesis(initial_transactions)
    
    def user_wallet_check(self, user_pk: str):
        user_coins = []
        for block in self.__chain:
            for transaction in block.transactions:
                if transaction.get_recipient_pk() == user_pk:
                    user_coins.append(transaction.coin)
                elif transaction.get_sender_pk() == user_pk:
                    user_coins = [
                        coin for coin in user_coins if coin.coin_id != transaction.coin.coin_id]
        return user_coins

    def create_genesis(self, initial_transactions):
        genesis_block = Block(0, initial_transactions, 0)
        self.__chain.append(genesis_block)
    
    def change_difficulty_level(self, level):
        self.__difficulty = level

    def add_block(self, block):
        if self.validate_block(block, self.last_block):
            self.__chain.append(block)
            return True
        
        return False

    def validate_block(self, current_block, previous_block):
        if current_block.index != previous_block.index + 1:
            return False

        if current_block.previous_hash != previous_block.hash:
            return False

        if not self.validate_proof_of_work(current_block.transactions, current_block.nonce):
            return False

        return True

    def append_blockchain(self, transactions: List[Transaction]):
        last_block = self.last_block
        index = last_block.index + 1
        nonce = self.generate_proof_of_work(transactions)
        block = Block(index, transactions, nonce, last_block)
        if self.add_block(block):
            return block
        
        return None

    def validate_proof_of_work(self, transactions: List[Transaction], nonce: int):
        target = pow(2, 256 - self.__difficulty)
        sha = hashlib.sha256(f'{transactions}{nonce}'.encode())
        return int(sha.hexdigest()[:self.__difficulty], base=16) < target

    def generate_proof_of_work(self, transactions: List[Transaction]):
        computing_power_random_variable = random.uniform(0, 10000)
        nonce = computing_power_random_variable
        while not self.validate_proof_of_work(transactions, nonce):
            nonce += 1

        return nonce

    def validate_chain(self, chain_to_validate):
        if chain_to_validate[0].hash != self.__chain[0].hash:
            return False

        for x in range(1, len(chain_to_validate)):
            if not self.validate_block(chain_to_validate[x], chain_to_validate[x - 1]):
                return False

        return True
