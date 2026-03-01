import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

@st.cache_data(ttl=300)
def get_stock_data(symbol):
    stock = yf.Ticker(symbol)
    return stock.history(period="3mo")
st.set_page_config(page_title="Ramkesh Pro Dashboard", layout="wide")

st.title("📊 Ramkesh Pro Stock Dashboard")

menu = st.sidebar.selectbox(
    "Navigation",
    ["Dashboard", "Stock Analysis"]
)

# ---------------- DASHBOARD ----------------
if menu == "Dashboard":

    st.header("📈 Market Overview")

    nifty = yf.Ticker("^NSEI")
    data = nifty.history(period="1d")

    if not data.empty:
        current = data["Close"].iloc[-1]
        open_price = data["Open"].iloc[-1]
        change = current - open_price
        percent = (change / open_price) * 100

        st.metric("NIFTY 50", f"{round(current,2)}", f"{round(percent,2)}%")

# ---------------- STOCK ANALYSIS ----------------
elif menu == "Stock Analysis":

    symbol = st.text_input("Enter NSE Symbol (Example: RELIANCE.NS)")

    if symbol:
        stock = yf.Ticker(symbol)
        data = stock.history(period="3mo")

        if not data.empty:

            fig = go.Figure(data=[go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close']
            )])

            fig.update_layout(
                xaxis_rangeslider_visible=False,
                template="plotly_dark"
            )

            st.plotly_chart(fig, use_container_width=True)

        else:
            st.error("Invalid symbol")
