import yfinance as yf
from ta.momentum import RSIIndicator

# STOCK LIST
stocks = ["TCS", "INFY", "RELIANCE", "SBIN"]

# USER INPUT
max_price = float(input("Enter Maximum Price: "))

print("\n====== NSE AI RSI SCANNER ======\n")

for stock_name in stocks:

    symbol = stock_name + ".NS"

    stock = yf.Ticker(symbol)

    # 14 DAYS DATA
    data = stock.history(period="14d")

    latest = data.iloc[-1]

    close_price = latest['Close']
    volume = latest['Volume']

    # RSI CALCULATION
    rsi = RSIIndicator(data['Close']).rsi()
    latest_rsi = rsi.iloc[-1]

    # TREND
    if latest_rsi > 70:
        momentum = "Overbought"

    elif latest_rsi < 30:
        momentum = "Oversold"

    else:
        momentum = "Strong"

    # FILTER
    if close_price < max_price:

        print(f"\nStock : {stock_name}")
        print(f"Price : ₹ {close_price:.2f}")
        print(f"Volume : {volume}")
        print(f"RSI : {latest_rsi:.2f}")
        print(f"Momentum : {momentum}")

        print("-----------------------------------")