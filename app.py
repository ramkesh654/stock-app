import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(page_title="Ramkesh Pro Dashboard", layout="wide")

# -------- CACHE FUNCTIONS --------
@st.cache_data(ttl=600)
def get_stock_data(symbol):
    stock = yf.Ticker(symbol)
    return stock.history(period="3mo")

@st.cache_data(ttl=600)
def get_nifty_data():
    nifty = yf.Ticker("^NSEI")
    return nifty.history(period="1d")

# -------- TITLE --------
st.title("📊 Ramkesh Pro Stock Dashboard")

# -------- SIDEBAR --------
menu = st.sidebar.selectbox(
    "Navigation",
    ["Dashboard", "Stock Analysis"]
)

# ---------------- DASHBOARD ----------------
if menu == "Dashboard":

    st.header("📈 Market Overview")

    try:
        data = get_nifty_data()

        if not data.empty:
            current = data["Close"].iloc[-1]
            open_price = data["Open"].iloc[-1]
            change = current - open_price
            percent = (change / open_price) * 100

            st.metric("NIFTY 50", f"{round(current,2)}", f"{round(percent,2)}%")
        else:
            st.warning("No data available")

    except:
        st.error("Market data temporarily unavailable. Try again later.")

# ---------------- STOCK ANALYSIS ----------------
elif menu == "Stock Analysis":

    symbol = st.text_input("Enter NSE Symbol (Example: TCS.NS)")

    if symbol:
        try:
            data = get_stock_data(symbol.upper())

            if not data.empty:

                st.subheader("📊 Candlestick Chart")

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
                st.error("Invalid symbol or no data available")

        except:
            st.error("Too many requests. Please wait 5 minutes and try again.")
