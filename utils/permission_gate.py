import time
class PermissionGate:
    def __init__(self, tg):
        self.tg = tg
    def ask(self, coin, direction, period, price, data):
        msg = f"AUTO-APPROVED – {coin} {direction} @ EMA{period} = ${price}"
        self.tg.send(msg)
        time.sleep(3)
        return True
