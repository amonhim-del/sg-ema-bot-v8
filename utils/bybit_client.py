import json
from pybit.unified_trading import HTTP

class BybitClient:
    def __init__(self, testnet=True):
        with open("config/secrets.json") as f:
            secrets = json.load(f)
        self.session = HTTP(
            testnet=testnet,
            api_key=secrets["bybit_api_key"],
            api_secret=secrets["bybit_api_secret"]
        )
        self.equity = float(self.session.get_wallet_balance(coin="USDT")["result"]["totalEquity"])

    def get_price(self, symbol):
        tick = self.session.get_tickers(category="linear", symbol=symbol)
        return float(tick["result"]["list"][0]["lastPrice"])

    def get_equity(self):
        bal = self.session.get_wallet_balance(coin="USDT")
        self.equity = float(bal["result"]["totalEquity"])
        return self.equity

    def tighten_all_sl(self, percent):
        positions = self.session.get_positions(category="linear", settleCoin="USDT")["result"]["list"]
        for pos in positions:
            if float(pos["size"]) == 0: continue
            entry = float(pos["avgPrice"])
            side = pos["side"]
            new_sl = entry * (1 - percent * (1 if side == "Buy" else -1))
            self.session.set_trading_stop(
                category="linear",
                symbol=pos["symbol"],
                stopLoss=round(new_sl, 2),
                positionIdx=0
            )

    def place_limit(self, coin, direction, price, data):
        symbol = data["symbol"]
        qty = (self.equity * data["risk_percent"] / 100) / price * data["leverage"]
        self.session.place_order(
            category="linear",
            symbol=symbol,
            side="Buy" if direction == "Long" else "Sell",
            orderType="Limit",
            qty=round(qty, 3),
            price=round(price, 2),
            timeInForce="PostOnly",
            reduceOnly=False,
            closeOnTrigger=False
        )
