import yfinance as yf
import ta
import requests
import schedule
import time
from datetime import datetime

# === CONFIG ===
BANKNIFTY_SYMBOL = "^NSEBANK"
WEBHOOK_URL = "https://banknifty-bot-50v4.onrender.com/webhook"

def fetch_data():
    df = yf.download(tickers=BANKNIFTY_SYMBOL, interval="5m", period="1d")
    df.dropna(inplace=True)
    return df

def analyze_and_send():
    df = fetch_data()

    # Indicators
    df['EMA20'] = ta.trend.ema_indicator(df['Close'], window=20).round(2)
    df['EMA50'] = ta.trend.ema_indicator(df['Close'], window=50).round(2)
    df['RSI'] = ta.momentum.rsi(df['Close'], window=14).round(2)

    latest = df.iloc[-1]
    price = latest['Close']
    ema20 = latest['EMA20']
    ema50 = latest['EMA50']
    rsi = latest['RSI']

    signal = ""
    if price > ema20 > ema50 and rsi > 60:
        signal = f"""📈 *BANKNIFTY Scalping Signal (Buy)*  
Buy Above: {price}  
Target: {price + 50}, {price + 80}  
SL: {price - 30}  
Reason: Price > EMA20 & EMA50 + RSI {rsi}"""

    elif price < ema20 < ema50 and rsi < 40:
        signal = f"""📉 *BANKNIFTY Scalping Signal (Sell)*  
Sell Below: {price}  
Target: {price - 50}, {price - 80}  
SL: {price + 30}  
Reason: Price < EMA20 & EMA50 + RSI {rsi}"""

    if signal:
        print("✅ Signal found, sending to Telegram...")
        requests.post(WEBHOOK_URL, json={"text": signal})
    else:
        print("❌ No valid signal found.")

# Run every 5 mins
schedule.every(5).minutes.do(analyze_and_send)

print("🚀 Bot started. Waiting for signal...")
while True:
    schedule.run_pending()
    time.sleep(1)
