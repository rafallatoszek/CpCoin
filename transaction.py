from coin import Coin
from utils import generate_transaction_data, transaction_to_bytes

class Transaction:
    def __init__(self, sender_pk: bytes, recipient_pk: bytes, coin: Coin):
        self.sender_pk = sender_pk
        self.recipient_pk = recipient_pk
        self.coin = coin

    def generate_data(self) -> bytes:
        transaction_data = generate_transaction_data(str(self.sender_pk), str(self.recipient_pk), self.coin.coin_id)
        return transaction_to_bytes(transaction_data)

    def set_signature(self, signature: bytes):
        self.signature = signature

    def get_sender_pk(self):
        return str(self.sender_pk)
    
    def get_recipient_pk(self):
        return str(self.recipient_pk)

    def __str__(self):
        return "Sender: " + str(self.sender_pk) + "\nRecipient: " + str(self.recipient_pk) + "\Coin: " + str(self.coin.coin_id)