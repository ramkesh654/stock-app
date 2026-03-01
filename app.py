import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Ramkesh Pro Dashboard", layout="wide")

st.title("📊 Ramkesh Pro Stock Dashboard")

# -------- Sidebar Navigation --------
menu = st.sidebar.selectbox(
    "Navigation",
    ["Dashboard", "Stock Analysis", "Market Movers", "Portfolio"]
)

# ---------------- DASHBOARD ----------------
if menu == "Dashboard":

    st.header("📈 Market Overview")

    nifty = yf.Ticker("^NSEI")
    nifty_data = nifty.history(period="1d")

    if not nifty_data.empty:
        current = nifty_data["Close"].iloc[-1]
        open_price = nifty_data["Open"].iloc[-1]
        change = current - open_price
        percent = (change / open_price) * 100

        st.metric("NIFTY 50", f"{round(current,2)}", f"{round(percent,2)}%")

# ---------------- STOCK ANALYSIS ----------------
elif menu == "Stock Analysis":

    symbol = st.text_input("Enter NSE Symbol (Example: RELIANCE.NS)")

    if symbol:
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            data = stock.history(period="3mo")

            col1, col2, col3 = st.columns(3)
            col1.metric("Current Price", f"₹ {info.get('currentPrice','N/A')}")
            col2.metric("Day High", f"₹ {info.get('dayHigh','N/A')}")
            col3.metric("Day Low", f"₹ {info.get('dayLow','N/A')}")

            st.write("### Company Name")
            st.write(info.get("longName", "Not Available"))

            st.write("### 3 Month Chart")
            st.line_chart(data["Close"])

        except:
            st.error("Invalid symbol")

# ---------------- MARKET MOVERS ----------------
elif menu == "Market Movers":

    st.header("🔥 Sample NSE Movers")

    stocks = ["RELIANCE.NS","TCS.NS","INFY.NS","HDFCBANK.NS","ICICIBANK.NS"]

    for s in stocks:
        data = yf.Ticker(s).history(period="1d")
        if not data.empty:
            open_price = data["Open"].iloc[-1]
            close_price = data["Close"].iloc[-1]
            change = ((close_price - open_price) / open_price) * 100
            st.write(f"{s} → {round(change,2)} %")

# ---------------- PORTFOLIO ----------------
elif menu == "Portfolio":

    st.header("💼 Portfolio Calculator")

    symbol = st.text_input("Stock Symbol")
    quantity = st.number_input("Quantity", min_value=1, step=1)
    buy_price = st.number_input("Buy Price (₹)", min_value=1.0)

    if symbol:
        try:
            current_data = yf.Ticker(symbol).history(period="1d")
            if not current_data.empty:
                current_price = current_data["Close"].iloc[-1]

                total_investment = quantity * buy_price
                current_value = quantity * current_price
                profit_loss = current_value - total_investment
                percent = (profit_loss / total_investment) * 100

                st.metric("Current Price", f"₹ {round(current_price,2)}")
                st.metric("Profit/Loss", f"₹ {round(profit_loss,2)} ({round(percent,2)}%)")

        except:
            st.error("Error loading data")
