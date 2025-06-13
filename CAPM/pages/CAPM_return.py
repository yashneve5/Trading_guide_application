# --- Import Libraries ---
import streamlit as st
import pandas as pd
import yfinance as yf
import pandas_datareader.data as web
import datetime
import capm_functions as capm_functions

# --- Page Config ---
st.set_page_config(
    page_title="CAPM",
    page_icon="📈",
    layout='wide'
)

# --- Custom Styling ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            background-color: #0e1117;
            color: #FFFFFF;
        }

        h1, h2, h3 {
            color: #00f2a6;
        }

        .stNumberInput label, .stMultiSelect label {
            font-weight: 600;
            color: #a8f8ff;
        }

        .stDataFrame {
            background-color: #1c1f26;
            border-radius: 10px;
            padding: 10px;
        }

        .reportview-container .main .block-container {
            padding-top: 2rem;
        }

        .stButton>button {
            background-color: #00f2a6;
            color: black;
        }
    </style>
""", unsafe_allow_html=True)

# --- Inputs UI ---
st.markdown("## 📊 Capital Asset Pricing Model (CAPM) Calculator")
st.markdown("Use this tool to analyze stock betas and expected returns using the CAPM formula.")

col1, col2 = st.columns([1, 1])
with col1:
    stocks_list = st.multiselect(
        "Choose up to 4 stocks",
        ('TSLA', 'AAPL', 'NFLX', 'MSFT', 'MGM', 'AMZN', 'NVDA', 'GOOGL'),
        ['TSLA', 'AAPL', 'AMZN', 'GOOGL']
    )
with col2:
    year = st.number_input("Number of years", 1, 10, value=3)

# --- Download Data ---
try:
    end = datetime.date.today()
    start = datetime.date(end.year - year, end.month, end.day)

    SP500 = web.DataReader(['sp500'], 'fred', start, end)

    stocks_df = pd.DataFrame()
    for stock in stocks_list:
        data = yf.download(stock, period=f'{year}y')
        stocks_df[stock] = data['Close']

    stocks_df.reset_index(inplace=True)
    SP500.reset_index(inplace=True)
    SP500.columns = ['Date', 'sp500']
    stocks_df['Date'] = pd.to_datetime(stocks_df['Date'].astype(str).str[:10])
    stocks_df = pd.merge(stocks_df, SP500, on='Date', how='inner')

    # --- Show Raw Data ---
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### 🧾 DataFrame Head")
        st.dataframe(stocks_df.head(), use_container_width=True)
    with col2:
        st.markdown("### 🧾 DataFrame Tail")
        st.dataframe(stocks_df.tail(), use_container_width=True)

    # --- Price Charts ---
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### 📉 Stock Prices")
        st.plotly_chart(capm_functions.interactive_plot(stocks_df), use_container_width=True)
    with col2:
        st.markdown("### 📈 Normalized Prices")
        normalized_df = capm_functions.normalize(stocks_df)
        st.plotly_chart(capm_functions.interactive_plot(normalized_df), use_container_width=True)

    # --- Calculate Daily Returns ---
    stocks_daily_return = capm_functions.daily_return(stocks_df)

    beta = {}
    alpha = {}
    for i in stocks_daily_return.columns:
        if i not in ['Date', 'sp500']:
            b, a = capm_functions.calculate_beta(stocks_daily_return, i)
            beta[i] = b
            alpha[i] = a

    # --- Beta Table ---
    beta_df = pd.DataFrame({
        'Stock': list(beta.keys()),
        'Beta Value': [round(b, 2) for b in beta.values()]
    })

    with col1:
        st.markdown("### 🧮 Calculated Beta Values")
        st.dataframe(beta_df, use_container_width=True)

    # --- Return using CAPM ---
    rf = 0  # risk-free rate
    rm = stocks_daily_return['sp500'].mean() * 252

    return_df = pd.DataFrame({
        'Stock': list(beta.keys()),
        'Expected Return (%)': [round(rf + (b * (rm - rf)), 2) for b in beta.values()]
    })

    with col2:
        st.markdown("### 💹 Expected Returns (CAPM)")
        st.dataframe(return_df, use_container_width=True)

except Exception as e:
    st.error("⚠️ Please select valid inputs or check your internet connection.")

