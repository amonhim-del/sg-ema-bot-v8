class EMACalculator:
    def __init__(self):
        self.yesterday_emas = {}
        self.filled_today = {}

    def get_live_daily_emas(self, coin, current_price):
        alphas = {50: 2/51, 100: 2/101, 150: 2/151, 200: 2/201}
        live_emas = {}
        for period, alpha in alphas.items():
            prev = self.yesterday_emas.get(coin, {}).get(period, current_price)
            live_emas[period] = round((current_price * alpha) + (prev * (1 - alpha)), 2)
        return live_emas

    def reset_daily(self):
        self.yesterday_emas = {}
        self.filled_today.clear()
