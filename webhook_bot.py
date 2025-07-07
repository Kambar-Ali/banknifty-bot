from flask import Flask, request
import requests

app = Flask(__name__)

TELEGRAM_TOKEN = "7668882475:AAFuqJyYU1p7RTLg6-gMfghMfZq1Tc7DZtA"
CHAT_ID = "6930983249"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    message = data.get("text", "⚠️ No message content found.")
    
    send_to_telegram(message)
    return '✅ Message Sent to Telegram!', 200

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, json=payload)

if __name__ == '__main__':
    print("🚀 Flask server starting...")
    app.run(debug=True)
