import streamlit as st 
import pandas as pd
import yfinance as yf 
import plotly.graph_objects as go 
import datetime 
import ta
from pages.utils.plotly_figure import plotly_table 
from pages.utils.plotly_figure import candlestick, RSI, MACD, Moving_average, close_chart
from pages.utils.plotly_figure import filter_data

# Setting page config 
st.set_page_config(
    page_title="Stock Analysis",
    page_icon="📊",
    layout='wide',
) 

# Enhanced CSS to completely remove dividers and improve structure
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* COMPLETE DIVIDER REMOVAL */
    hr, .stMarkdown hr, .block-container hr {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        border: none !important;
    }
    
    /* Remove all Streamlit default dividers and separators */
    .main .block-container {
        padding-top: 0.5rem;
        padding-bottom: 0rem;
        max-width: none;
        gap: 0 !important;
    }
    
    .element-container {
        margin: 0 !important;
        padding: 0 !important;
        gap: 0 !important;
    }
    
    /* Remove spacing between elements */
    .stMarkdown, .stPlotlyChart, .stDataFrame, .stMetric, .stSelectbox, .stTextInput, .stDateInput, .stButton {
        margin: 0 !important;
        margin-bottom: 0 !important;
        margin-top: 0 !important;
        padding-bottom: 0 !important;
        border: none !important;
    }
    
    /* Remove any possible divider elements */
    .stMarkdown > div:empty,
    .element-container:empty,
    .block-container > div:empty {
        display: none !important;
    }
    
    /* Hide horizontal rules in markdown */
    .stMarkdown div[data-testid="stMarkdownContainer"] hr {
        display: none !important;
    }
    
    /* Main background */
    .main {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Title styling */
    .main-title {
        background: linear-gradient(135deg, #00ff88 0%, #00cc6a 50%, #ffffff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin: 1rem 0 2rem 0;
        text-shadow: 0 0 30px rgba(0,255,136,0.5);
    }
    
    /* Container styles with no gaps */
    .custom-container {
        background: rgba(25,25,45,0.95);
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid rgba(0,255,136,0.3);
        margin: 0.8rem 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    
    /* Seamless section transitions */
    .seamless-section {
        background: rgba(25,25,45,0.95);
        padding: 1.2rem;
        border-radius: 12px;
        border: 1px solid rgba(0,255,136,0.25);
        margin: 0.5rem 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 6px 25px rgba(0,0,0,0.2);
        position: relative;
        overflow: hidden;
    }
    
    .seamless-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, transparent, #00ff88, transparent);
        animation: shine 3s infinite;
    }
    
    @keyframes shine {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .section-title {
        color: #00ff88;
        font-size: 1.3rem;
        font-weight: 600;
        margin: 0 0 1rem 0;
        text-align: center;
        text-shadow: 0 0 10px rgba(0,255,136,0.4);
        position: relative;
    }
    
    .section-title::after {
        content: '';
        position: absolute;
        bottom: -5px;
        left: 50%;
        transform: translateX(-50%);
        width: 50px;
        height: 2px;
        background: linear-gradient(90deg, transparent, #00ff88, transparent);
    }
    
    /* Input styling */
    .stTextInput > div > div > input,
    .stDateInput > div > div > input {
        background: rgba(30,30,50,0.8) !important;
        border: 2px solid rgba(0,255,136,0.4) !important;
        border-radius: 10px !important;
        color: #ffffff !important;
        font-weight: 500 !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stDateInput > div > div > input:focus {
        border-color: #00ff88 !important;
        box-shadow: 0 0 15px rgba(0,255,136,0.3) !important;
    }
    
    .stSelectbox > div > div {
        background: rgba(30,30,50,0.8) !important;
        border: 2px solid rgba(0,255,136,0.4) !important;
        border-radius: 10px !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, rgba(0,255,136,0.1), rgba(0,255,136,0.05)) !important;
        color: #00ff88 !important;
        border: 2px solid rgba(0,255,136,0.4) !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #00ff88, #00cc6a) !important;
        color: #000000 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 25px rgba(0,255,136,0.3) !important;
    }
    
    /* Metric cards */
    .metric-container {
        background: rgba(25,25,45,0.8);
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid rgba(0,255,136,0.3);
        text-align: center;
        margin: 0.5rem 0;
    }
    
    /* Stock ticker display */
    .stock-ticker {
        background: linear-gradient(135deg, #00ff88 0%, #00cc6a 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.2rem;
        font-weight: 700;
        text-align: center;
        margin: 1rem 0;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
    }
    
    .stock-logo {
        width: 50px;
        height: 50px;
        border-radius: 10px;
        border: 2px solid rgba(0,255,136,0.3);
    }
    
    /* Company info */
    .company-summary {
        background: rgba(25,25,45,0.6);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #00ff88;
        color: #e0e0e0;
        line-height: 1.6;
        margin: 1rem 0;
    }
    
    .company-detail {
        background: rgba(25,25,45,0.4);
        padding: 1rem;
        border-radius: 8px;
        color: #b8b8d4;
        margin: 0.5rem 0;
    }
    
    /* Chart containers */
    .chart-wrapper {
        background: rgba(25,25,45,0.3);
        padding: 1rem;
        border-radius: 15px;
        border: 1px solid rgba(0,255,136,0.2);
        margin: 1rem 0;
    }
    
    /* Remove plotly chart margins */
    .js-plotly-plot {
        margin: 0 !important;
    }
    
    /* Floating animation elements */
    .floating-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
        overflow: hidden;
    }
    
    .float-element {
        position: absolute;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(0,255,136,0.1), transparent);
        animation: float 8s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) scale(1); opacity: 0.3; }
        50% { transform: translateY(-30px) scale(1.1); opacity: 0.6; }
    }
</style>
""", unsafe_allow_html=True)

# Animated background elements
st.markdown("""
<div class="floating-bg">
    <div class="float-element" style="width: 100px; height: 100px; top: 10%; left: 85%; animation-delay: 0s;"></div>
    <div class="float-element" style="width: 60px; height: 60px; top: 30%; left: 5%; animation-delay: 2s;"></div>
    <div class="float-element" style="width: 80px; height: 80px; top: 70%; left: 90%; animation-delay: 4s;"></div>
    <div class="float-element" style="width: 50px; height: 50px; top: 85%; left: 8%; animation-delay: 6s;"></div>
</div>
""", unsafe_allow_html=True)

# Main title
st.markdown('<h1 class="main-title">📊 Stock Analysis Dashboard</h1>', unsafe_allow_html=True)

# Input section - seamless design
st.markdown('<div class="seamless-section">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🎯 Stock Configuration</div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

today = datetime.date.today()

with col1:
    ticker = st.text_input("🎯 Stock Ticker", "TSLA", key="ticker_input")
with col2:
    start_date = st.date_input("📅 Start Date", datetime.date(today.year - 1, today.month, today.day))
with col3:
    end_date = st.date_input("📅 End Date", datetime.date(today.year, today.month, today.day))
st.markdown('</div>', unsafe_allow_html=True)

# Stock ticker display with logo
try:
    stock = yf.Ticker(ticker)
    logo_url = f"https://logo.clearbit.com/{stock.info.get('website', '').replace('https://','').replace('http://','').split('/')[0]}"
    st.markdown(f'''
    <div class="stock-ticker">
        <img src="{logo_url}" class="stock-logo" onerror="this.style.display='none'" alt="{ticker} logo">
        {ticker}
    </div>
    ''', unsafe_allow_html=True)
except:
    st.markdown(f'<div class="stock-ticker">{ticker}</div>', unsafe_allow_html=True)

# Company overview - seamless design
st.markdown('<div class="seamless-section">', unsafe_allow_html=True)
st.markdown('<div class="section-title">💼 Company Overview</div>', unsafe_allow_html=True)
try:
    business_summary = stock.info.get("longBusinessSummary", "Business summary not available for this ticker.")
    st.markdown(f'<div class="company-summary">{business_summary}</div>', unsafe_allow_html=True)
except:
    st.markdown('<div class="company-summary">Business summary not available for this ticker.</div>', unsafe_allow_html=True)

# Company details in a single row
col1, col2, col3 = st.columns(3)
with col1:
    try:
        sector = stock.info.get("sector", "N/A")
        st.markdown(f'<div class="company-detail"><strong>🏢 Sector:</strong><br>{sector}</div>', unsafe_allow_html=True)
    except:
        st.markdown('<div class="company-detail"><strong>🏢 Sector:</strong><br>N/A</div>', unsafe_allow_html=True)

with col2:
    try:
        employees = stock.info.get("fullTimeEmployees", 0)
        if employees:
            st.markdown(f'<div class="company-detail"><strong>👥 Employees:</strong><br>{employees:,}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="company-detail"><strong>👥 Employees:</strong><br>N/A</div>', unsafe_allow_html=True)
    except:
        st.markdown('<div class="company-detail"><strong>👥 Employees:</strong><br>N/A</div>', unsafe_allow_html=True)

with col3:
    try:
        website = stock.info.get("website", "")
        if website:
            st.markdown(f'<div class="company-detail"><strong>🌐 Website:</strong><br><a href="{website}" target="_blank" style="color: #00ff88; text-decoration: none;">{website}</a></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="company-detail"><strong>🌐 Website:</strong><br>N/A</div>', unsafe_allow_html=True)
    except:
        st.markdown('<div class="company-detail"><strong>🌐 Website:</strong><br>N/A</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Financial metrics - seamless design
st.markdown('<div class="seamless-section">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📊 Financial Metrics</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    try:
        df = pd.DataFrame(index=['Market Cap', 'Beta', 'EPS', 'PE Ratio'])
        df['Value'] = [
            stock.info.get("marketCap", "N/A"), 
            stock.info.get("beta", "N/A"),
            stock.info.get("trailingEps", "N/A"), 
            stock.info.get("trailingPE", "N/A")
        ]
        fig_df = plotly_table(df)
        st.plotly_chart(fig_df, use_container_width=True)
    except:
        st.write("Financial metrics not available")

with col2:
    try:
        df = pd.DataFrame(index=['Quick Ratio', 'Revenue per Share', 'Profit Margins', 'Debt to Equity', 'Return on Equity'])
        df['Value'] = [
            stock.info.get("quickRatio", "N/A"), 
            stock.info.get("revenuePerShare", "N/A"),
            stock.info.get("profitMargins", "N/A"), 
            stock.info.get("debtToEquity", "N/A"),
            stock.info.get("returnOnEquity", "N/A")
        ]
        fig_df = plotly_table(df)
        st.plotly_chart(fig_df, use_container_width=True)
    except:
        st.write("Additional metrics not available")
st.markdown('</div>', unsafe_allow_html=True)

# Get stock data
data = yf.download(ticker, start=start_date, end=end_date)

# Daily metrics - seamless design
st.markdown('<div class="seamless-section">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📈 Market Summary</div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
try:
    daily_change = data['Close'].iloc[-1] - data['Close'].iloc[-2]
    with col1:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("📈 Daily Change", f"${data['Close'].iloc[-1]:.2f}", f"{daily_change:.2f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("📊 Volume", f"{data['Volume'].iloc[-1]:,.0f}", "")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        high_52 = data['High'].rolling(window=252).max().iloc[-1]
        st.metric("🎯 52W High", f"${high_52:.2f}", "")
        st.markdown('</div>', unsafe_allow_html=True)
except:
    with col1:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("📈 Daily Change", "N/A", "N/A")
        st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Historical data table - seamless design
st.markdown('<div class="seamless-section">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📋 Recent Trading Data</div>', unsafe_allow_html=True)
last_10_df = data.tail(10).sort_index(ascending=False).round(3)
fig_df = plotly_table(last_10_df)
st.plotly_chart(fig_df, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Chart controls - seamless design
st.markdown('<div class="seamless-section">', unsafe_allow_html=True)
st.markdown('<div class="section-title">⏱️ Chart Controls</div>', unsafe_allow_html=True)

# Time period buttons
col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
num_period = ''

with col1:
    if st.button('5D', key='5d'):
        num_period = '5d'
with col2:
    if st.button('1M', key='1m'):
        num_period = '1mo'
with col3:
    if st.button('6M', key='6m'):
        num_period = '6mo'
with col4:
    if st.button('YTD', key='ytd'):
        num_period = 'ytd'
with col5:
    if st.button('1Y', key='1y'):
        num_period = '1y'
with col6:
    if st.button('5Y', key='5y'):
        num_period = '5y'
with col7:
    if st.button('MAX', key='max'):
        num_period = 'max'

# Chart configuration
col1, col2 = st.columns(2)
with col1:
    chart_type = st.selectbox('📈 Chart Type', ('Candle', 'Line'), key='chart_type')
with col2:
    if chart_type == 'Candle':
        indicators = st.selectbox('🔧 Indicators', ('RSI', 'MACD'), key='indicators_candle')
    else:
        indicators = st.selectbox('🔧 Indicators', ('RSI', 'Moving Average', 'MACD'), key='indicators_line')
st.markdown('</div>', unsafe_allow_html=True)

# Chart display - seamless design
st.markdown('<div class="seamless-section">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📊 Technical Analysis</div>', unsafe_allow_html=True)
# Get chart data
ticker_ = yf.Ticker(ticker)
new_df1 = ticker_.history(period='max')
data1 = ticker_.history(period='max')

# Default to 1 year if no period selected
period_to_use = num_period if num_period else '1y'
data_to_use = new_df1 if num_period else data1

# Chart logic
if chart_type == 'Candle':
    st.plotly_chart(candlestick(data_to_use, period_to_use), use_container_width=True)
    if indicators == 'RSI':
        st.plotly_chart(RSI(data_to_use, period_to_use), use_container_width=True)
    elif indicators == 'MACD':
        st.plotly_chart(MACD(data_to_use, period_to_use), use_container_width=True)
else:  # Line chart
    if indicators == 'Moving Average':
        st.plotly_chart(Moving_average(data_to_use, period_to_use), use_container_width=True)
    else:
        st.plotly_chart(close_chart(data_to_use, period_to_use), use_container_width=True)
        if indicators == 'RSI':
            st.plotly_chart(RSI(data_to_use, period_to_use), use_container_width=True)
        elif indicators == 'MACD':
            st.plotly_chart(MACD(data_to_use, period_to_use), use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #666; font-size: 0.9rem;">
    <p>📊 Built with Streamlit & yfinance | Real-time stock data visualization</p>
</div>
""", unsafe_allow_html=True)