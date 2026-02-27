import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Ramkesh Pro Dashboard", layout="wide")

st.title("📊 Ramkesh Pro Stock Dashboard")

# Sidebar
st.sidebar.header("Stock Search")
symbol = st.sidebar.text_input("Enter NSE Symbol (Example: RELIANCE.NS)")

if symbol:

    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        data = stock.history(period="1mo")

        col1, col2, col3 = st.columns(3)

        col1.metric("Current Price", f"₹ {info['currentPrice']}")
        col2.metric("Day High", f"₹ {info['dayHigh']}")
        col3.metric("Day Low", f"₹ {info['dayLow']}")

        st.subheader("Company Name")
        st.write(info.get("longName", "Not Available"))

        st.subheader("1 Month Price Chart")
        st.line_chart(data["Close"])

    except:
        st.error("Invalid symbol or data not available")
