class BybitClient:
    def __init__(self, testnet=True):
        self.testnet = testnet
        self.equity = 100000.0

    def get_price(self, symbol):
        return 103000.0

    def get_equity(self):
        return self.equity

    def tighten_all_sl(self, percent):
        pass

    def place_limit(self, coin, direction, price, data):
        pass
