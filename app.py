import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Ramkesh Pro Dashboard", layout="wide")

st.title("📊 Ramkesh Pro Stock Dashboard")

# ---------------- Sidebar ----------------
st.sidebar.header("🔍 Stock Search")
symbol = st.sidebar.text_input("Enter NSE Symbol (Example: RELIANCE.NS)")

# ---------------- Market Overview ----------------
st.header("📈 Market Overview")

nifty = yf.Ticker("^NSEI")
nifty_data = nifty.history(period="1d")

if not nifty_data.empty:
    current_nifty = nifty_data["Close"].iloc[-1]
    prev_close = nifty_data["Open"].iloc[-1]
    change = current_nifty - prev_close
    percent = (change / prev_close) * 100

    st.metric("NIFTY 50", f"{round(current_nifty,2)}", f"{round(percent,2)}%")

# ---------------- Stock Details ----------------
if symbol:
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        data = stock.history(period="1mo")

        st.header("📌 Stock Details")

        col1, col2, col3 = st.columns(3)
        col1.metric("Current Price", f"₹ {info.get('currentPrice','N/A')}")
        col2.metric("Day High", f"₹ {info.get('dayHigh','N/A')}")
        col3.metric("Day Low", f"₹ {info.get('dayLow','N/A')}")

        st.write("### Company Name")
        st.write(info.get("longName", "Not Available"))

        st.write("### 1 Month Price Chart")
        st.line_chart(data["Close"])

    except:
        st.error("Invalid symbol or data not available")

# ---------------- Top Movers ----------------
st.header("🔥 Top Movers (Sample NSE Stocks)")

stocks = ["RELIANCE.NS","TCS.NS","INFY.NS","HDFCBANK.NS","ICICIBANK.NS"]

gainers = []
losers = []

for s in stocks:
    data = yf.Ticker(s).history(period="1d")
    if not data.empty:
        open_price = data["Open"].iloc[-1]
        close_price = data["Close"].iloc[-1]
        change = ((close_price - open_price) / open_price) * 100
        if change > 0:
            gainers.append((s, round(change,2)))
        else:
            losers.append((s, round(change,2)))

col1, col2 = st.columns(2)

with col1:
    st.subheader("🚀 Gainers")
    for g in gainers:
        st.write(f"{g[0]}  →  {g[1]} %")

with col2:
    st.subheader("🔻 Losers")
    for l in losers:
        st.write(f"{l[0]}  →  {l[1]} %")

# ---------------- Portfolio Calculator ----------------
st.header("💼 Portfolio Calculator")

portfolio_symbol = st.text_input("Enter Stock for Portfolio (Example: RELIANCE.NS)")
quantity = st.number_input("Quantity", min_value=1, step=1)
buy_price = st.number_input("Buy Price (₹)", min_value=1.0)

if portfolio_symbol:
    try:
        current_data = yf.Ticker(portfolio_symbol).history(period="1d")
        if not current_data.empty:
            current_price = current_data["Close"].iloc[-1]

            total_investment = quantity * buy_price
            current_value = quantity * current_price
            profit_loss = current_value - total_investment
            percent_change = (profit_loss / total_investment) * 100

            col1, col2, col3 = st.columns(3)

            col1.metric("Current Price", f"₹ {round(current_price,2)}")
            col2.metric("Total Investment", f"₹ {round(total_investment,2)}")
            col3.metric("Current Value", f"₹ {round(current_value,2)}")

            if profit_loss >= 0:
                st.success(f"Profit: ₹ {round(profit_loss,2)} ({round(percent_change,2)}%)")
            else:
                st.error(f"Loss: ₹ {round(profit_loss,2)} ({round(percent_change,2)}%)")

    except:
        st.error("Portfolio data not available")
