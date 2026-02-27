import streamlit as st
import yfinance as yf

st.title("Live Stock Price 📈")

stock = st.text_input("Enter Stock Symbol (Example: RELIANCE.NS)")

if stock:
    data = yf.download(stock, period="1mo")

    st.subheader("Last 5 Days Data")
    st.write(data.tail())

    st.subheader("Closing Price Chart")
    st.line_chart(data["Close"])
