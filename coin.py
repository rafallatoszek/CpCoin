class Coin:
    def __init__(self, coin_id: int, value: int):
        self.coin_id = coin_id
        self.value = value

    def serialize(self):
        return self.__dict__
    
    def __str__(self):
        return str(self.coin_id)

    
