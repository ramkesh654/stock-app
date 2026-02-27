import streamlit as st
import yfinance as yf

st.title("Live Stock Price 📈")

stock = st.text_input("Enter Stock Symbol (Example: RELIANCE.NS)")

if stock:
    data = yf.download(stock, period="1d")
    st.write(data.tail())
