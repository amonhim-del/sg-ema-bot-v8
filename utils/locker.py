from datetime import datetime
class Locker:
    def __init__(self, tg, bybit, sheet):
        self.tg = tg
        self.bybit = bybit
        self.sheet = sheet
        self.reset_equity = 100000.0
        self.locked_percent = 0.0

    def run(self):
        settings_rows = self.sheet.locker.get_all_values()[1:]
        settings = {row[0].strip(): row[1].strip() for row in settings_rows if len(row) > 1}
        if settings.get("Max_Lock_At_Expected", "TRUE").upper() != "TRUE":
            return

        actual_pnl = (self.bybit.get_equity() / self.reset_equity - 1)
        day = datetime.utcnow().day
        expected_pnl = 0.05 * (day / 30.0)

        if actual_pnl > expected_pnl:
            lock_target = expected_pnl
            if lock_target > self.locked_percent:
                self.bybit.tighten_all_sl(lock_target)
                self.locked_percent = lock_target
                self.tg.send(f"LOCKER ACTIVATED — {lock_target:.2%} SECURED")
                self.tg.send(f"Pause new entries? (Default: CONTINUE in 30 min)")
