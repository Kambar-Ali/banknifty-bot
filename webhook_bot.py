from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Environment-safe credentials with fallback
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "7668882475:AAFuqJyYU1p7RTLg6-gMfghMfZq1Tc7DZtA")
CHAT_ID = os.getenv("CHAT_ID", "6930983249")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    # Extract message
    message = data.get("text", "⚠️ No message content found.")
    
    # Send to Telegram
    send_to_telegram(message)

    return '✅ Message Sent to Telegram!', 200

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    try:
        response = requests.post(url, json=payload)
        print("Telegram Response:", response.text)
    except Exception as e:
        print("Telegram Send Error:", e)

if __name__ == '__main__':
    print("🚀 Flask server starting...")
    port = int(os.environ.get("PORT", 10000))  # Render provides dynamic PORT
    app.run(host="0.0.0.0", port=port)
