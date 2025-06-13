import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
import numpy as np
import plotly.graph_objects as go

# Page Setup
st.set_page_config(page_title="Trading Guide App - CAPM Analysis", page_icon="📈", layout="wide")

# Custom CSS
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        html, body, [class*="css"]  {
            font-family: 'Inter', sans-serif;
            background: #0f0f23;
            color: #ffffff;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #00ff88;
        }
        .stSelectbox > div > div {
            background-color: #1a1a2e;
            border: 1px solid #00ff88;
            border-radius: 8px;
        }
        .stNumberInput > div > div > input {
            background-color: #1a1a2e;
            color: #ffffff;
            border: 1px solid #00ff88;
        }
        .highlight-text {
            transition: all 0.3s ease-in-out;
        }
        .highlight-text:hover {
            text-shadow: 0 0 20px #00ff88;
            color: #ffffff;
        }
    </style>
""", unsafe_allow_html=True)



# User Inputs
st.markdown("---")
st.markdown("### Select Stock and Time Frame")
col1, col2 = st.columns(2)
with col1:
    stock = st.selectbox("Choose a stock", ['TSLA', 'AAPL', 'NFLX', 'MSFT', 'MGM', 'AMZN', 'NVDA', 'GOOGL'], index=7)
with col2:
    year = st.number_input("Number of Years", min_value=1, max_value=10, value=3)

# Data Processing
try:
    end = datetime.date.today()
    start = datetime.date(end.year - year, end.month, end.day)

    # Get stock and SP500 data
    stock_data = yf.download(stock, start=start, end=end)
    sp500_data = yf.download('^GSPC', start=start, end=end)

    # Prepare the DataFrame
    df = pd.DataFrame()
    df['Stock'] = stock_data['Close']
    df['Market'] = sp500_data['Close']
    df.dropna(inplace=True)

    # Calculate Daily Returns
    df['Stock Return'] = df['Stock'].pct_change()
    df['Market Return'] = df['Market'].pct_change()
    df.dropna(inplace=True)

    # Calculate Beta using linear regression
    beta, alpha = np.polyfit(df['Market Return'], df['Stock Return'], 1)

    # Expected Return (CAPM)
    rf = 0  # Risk-free rate assumed 0%
    rm = df['Market Return'].mean() * 252  # Annualized
    expected_return = rf + beta * (rm - rf)

    # Output Results
    st.markdown(f"## 📈 Results for {stock}")
    st.success(f"**Beta : {round(beta, 4)}**")
    st.success(f"**Expected Annual Return : {round(expected_return * 100, 2)}%**")

    # Scatter plot with regression line
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['Market Return'],
        y=df['Stock Return'],
        mode='markers',
        name='Daily Returns',
        marker=dict(color='rgba(0,255,136,0.6)')
    ))

    reg_line = beta * df['Market Return'] + alpha
    fig.add_trace(go.Scatter(
        x=df['Market Return'],
        y=reg_line,
        mode='lines',
        name='Regression Line',
        line=dict(color='rgba(255,255,255,0.8)', width=2)
    ))

    fig.update_layout(
        title=f"{stock} vs Market Returns",
        xaxis_title="Market Return",
        yaxis_title=f"{stock} Return",
        plot_bgcolor='#0f0f23',
        paper_bgcolor='#0f0f23',
        font=dict(color='#ffffff')
    )

    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Something went wrong: {e}")
