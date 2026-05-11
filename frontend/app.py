import streamlit as st
import yfinance as yf
import pandas as pd

from ta.momentum import RSIIndicator
from openai import OpenAI

# -----------------------------------
# PAGE SETTINGS
# -----------------------------------

st.set_page_config(
    page_title="NSE AI Scanner",
    layout="wide"
)

# -----------------------------------
# OPENAI CLIENT
# -----------------------------------
client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)


# -----------------------------------
# TITLE
# -----------------------------------

st.title("📈 NSE AI Scanner Dashboard")

st.markdown("### Live NSE Market Intelligence System")

# -----------------------------------
# USER INPUT
# -----------------------------------

max_price = st.number_input(
    "Enter Maximum Price",
    value=2000
)

# -----------------------------------
# STOCK LIST
# -----------------------------------

# USER WATCHLIST

watchlist_input = st.text_input(

    "Enter NSE Stocks (comma separated)",

    "TCS,INFY,RELIANCE,SBIN"

)

# CONVERT INPUT TO LIST

stocks = [

    stock.strip().upper()

    for stock in watchlist_input.split(",")

]

# -----------------------------------
# STOCK DROPDOWN
# -----------------------------------

selected_stock = st.selectbox(
    "Select Stock For Chart",
    stocks
)

# -----------------------------------
# STORAGE VARIABLES
# -----------------------------------

results = []

scanner_summary = ""

# -----------------------------------
# MAIN SCANNER LOOP
# -----------------------------------

for stock_name in stocks:

    symbol = stock_name + ".NS"

    stock = yf.Ticker(symbol)

    data = stock.history(period="14d")

    # SAFETY CHECK
    if data.empty:
        continue

    latest = data.iloc[-1]

    close_price = latest['Close']

    volume = latest['Volume']

    # RSI CALCULATION
    rsi = RSIIndicator(data['Close']).rsi()

    latest_rsi = rsi.iloc[-1]

    # SIGNAL LOGIC
    if latest_rsi > 70:
        signal = "🔴 Overbought"

    elif latest_rsi < 30:
        signal = "🟡 Oversold"

    else:
        signal = "🟢 Strong"

    # FILTER
    if close_price < max_price:

        results.append({

            "Stock": stock_name,
            "Price": round(close_price, 2),
            "RSI": round(latest_rsi, 2),
            "Volume": int(volume),
            "Signal": signal
        })

        # AI SUMMARY DATA
        scanner_summary += f"""
Stock: {stock_name}
Price: {round(close_price,2)}
RSI: {round(latest_rsi,2)}
Signal: {signal}

"""

# -----------------------------------
# DATAFRAME
# -----------------------------------

df = pd.DataFrame(results)

# -----------------------------------
# KPI SECTION
# -----------------------------------

col1, col2, col3 = st.columns(3)

col1.metric("Stocks Scanned", len(stocks))

col2.metric("Matching Stocks", len(df))

col3.metric("Max Price Filter", max_price)

# -----------------------------------
# TABLE DISPLAY
# -----------------------------------

st.dataframe(df, use_container_width=True)

# -----------------------------------
# LIVE CHART SECTION
# -----------------------------------

st.markdown("## 📈 Live Stock Chart")

chart_symbol = selected_stock + ".NS"

chart_stock = yf.Ticker(chart_symbol)

chart_data = chart_stock.history(
    period="1d",
    interval="5m"
)

st.line_chart(chart_data['Close'])

# -----------------------------------
# AI CHAT SECTION
# -----------------------------------

st.markdown("## 🤖 AI Market Assistant")

user_question = st.text_input(
    "Ask AI About Market"
)

if st.button("Analyze"):

    response = client.chat.completions.create(

        model="gpt-4.1-mini",

        messages=[

            {
                "role": "system",

                "content": """

You are an advanced NSE market analyst AI assistant.

Your job:
- analyze live scanner data
- identify strongest stocks
- explain RSI
- identify bullish or bearish momentum
- explain signals clearly

Rules:
- Keep answers short
- Use bullet points
- Mention strongest stock first
- Mention RSI interpretation
- Mention momentum
- Give professional market insight

"""
            },

            {
                "role": "user",

                "content": f"""

User Question:
{user_question}

Live Scanner Data:
{scanner_summary}

Analyze this NSE market data carefully.

"""
            }

        ]
    )

    ai_reply = response.choices[0].message.content

    st.success(ai_reply)

# -----------------------------------
# FOOTER
# -----------------------------------

st.markdown("---")

st.write("AI Powered NSE Scanner | Developed by Mr. Kamra")