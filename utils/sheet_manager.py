import gspread
from oauth2client.service_account import ServiceAccountCredentials

class SheetManager:
    def __init__(self):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('service_account.json', scope)
        client = gspread.authorize(creds)
        self.doc = client.open_by_key("1VxIgrJMXQGmmAEIi77Glt62TZ9s2mUHSqJJBySZkSa8")
        self.pairs = self.doc.worksheet("PAIRS")
        self.positions = self.doc.worksheet("POSITIONS")
        self.locker = self.doc.worksheet("LOCKER_SETTINGS")
        self.rsi = self.doc.worksheet("RSI_SETTINGS")

    def get_pairs(self):
        rows = self.pairs.get_all_values()[1:]
        pairs = {}
        for row in rows:
            if len(row) >= 5 and row[2].upper() == "TRUE":
                pairs[row[0]] = {
                    "symbol": row[1],
                    "enabled": True,
                    "risk_percent": float(row[3]),
                    "leverage": int(row[4])
                }
        return pairs

    def get_positions(self):
        rows = self.positions.get_all_values()[1:]
        pos = {}
        for row in rows:
            if len(row) >= 5:
                pos[row[0]] = {50: row[1], 100: row[2], 150: row[3], 200: row[4]}
        return pos
