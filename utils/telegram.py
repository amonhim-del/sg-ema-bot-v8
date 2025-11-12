import requests
class TelegramNotifier:
    def __init__(self):
        self.token = "8590979765:AAG8nYtlTcq2ZFn--ZrprWkXvgCpkVkRXGI"
        self.chat_id = "1855283383"
    def send(self, msg):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        try:
            requests.post(url, data={"chat_id": self.chat_id, "text": msg}, timeout=10)
        except:
            pass
