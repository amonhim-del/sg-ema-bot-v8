import time
import schedule
from utils.sheet_manager import SheetManager
from utils.ema_calculator import EMACalculator
from utils.telegram import TelegramNotifier
from utils.bybit_client import BybitClient
from utils.permission_gate import PermissionGate
from utils.locker import Locker
from utils.dialogue_manager import DialogueManager
from utils.rsi_filter import RSIFilter

class SGEMABot:
    def __init__(self):
        self.tg = TelegramNotifier()
        self.sheet = SheetManager()
        self.ema = EMACalculator()
        self.bybit = BybitClient(testnet=True)
        self.permission = PermissionGate(self.tg)
        self.locker = Locker(self.tg, self.bybit, self.sheet)
        self.dialogue = DialogueManager(self.tg)
        self.rsi = RSIFilter(self.sheet)

        self.tg.send("SG EMA SILENT SHIELD v8.3 – TESTNET")
        self.tg.send("Profit Shield: PROPORTIONAL")
        self.tg.send("Pause dialogue: 30-min timeout → default CONTINUE")
        self.tg.send("Monthly PDF reports: ACTIVE")
        self.tg.send("First check in 4h...")

    def run(self):
        schedule.every(10).minutes.do(self.scan_and_place_limits)
        schedule.every(4).hours.do(self.locker.run)
        schedule.every().day.at("00:10").do(self.locker.daily_report)
        schedule.every().day.at("00:05").do(self.ema.reset_daily)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def scan_and_place_limits(self):
        pairs = self.sheet.get_pairs()
        positions = self.sheet.get_positions()
        for coin, data in pairs.items():
            if not data['enabled']: continue
            price = self.bybit.get_price(data['symbol'])
            emas = self.ema.get_live_daily_emas(coin, price)
            for period, value in emas.items():
                direction = positions.get(coin, {}).get(period)
                if direction and self.rsi.confirm(coin, direction):
                    if self.permission.ask(coin, direction, period, value, data):
                        self.bybit.place_limit(coin, direction, value, data)

if __name__ == "__main__":
    bot = SGEMABot()
    bot.run()
