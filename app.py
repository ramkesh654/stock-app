import plotly.graph_objects as go
from datetime import datetime

# ---------------- STOCK ANALYSIS ----------------
elif menu == "Stock Analysis":

    symbol = st.text_input("Enter NSE Symbol (Example: RELIANCE.NS)")

    if symbol:
        try:
            stock = yf.Ticker(symbol)
            data = stock.history(period="3mo")

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

        except:
            st.error("Invalid symbol")
