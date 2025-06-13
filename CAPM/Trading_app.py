import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Trading Guide App",
    page_icon="💹",
    layout="wide"
)

# Custom CSS Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, .main {
        height: 100%;
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        font-family: 'Inter', sans-serif;
    }

    .hero-section {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        min-height: 90vh;
        padding: 4rem 2rem;
        border-radius: 25px;
        margin: 0 auto 3rem auto;
        border: 1px solid rgba(0,255,136,0.2);
        background: linear-gradient(135deg, rgba(0,255,136,0.08), rgba(0,255,136,0.02));
        box-shadow: 0 20px 40px rgba(0,255,136,0.08);
        text-align: center;
        backdrop-filter: blur(8px);
    }

    .hero-title {
        font-size: 4.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #00ff88, #00cc6a, #ffffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        transition: all 0.3s ease-in-out;
        cursor: pointer;
        text-shadow: 0 0 20px rgba(0,255,136,0.4);
    }

    .hero-title:hover {
        text-shadow: 0 0 40px rgba(0,255,136,0.9);
        transform: scale(1.05);
    }

    .hero-subtitle {
        font-size: 1.6rem;
        color: #b8b8d4;
        margin-bottom: 1rem;
        font-weight: 300;
    }

    .feature-card, .navigation-menu {
        background: linear-gradient(145deg, rgba(30,30,46,0.8), rgba(45,45,68,0.8));
        padding: 2rem;
        border-radius: 20px;
        border: 1px solid rgba(0,255,136,0.3);
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
        margin: 1rem 0;
        backdrop-filter: blur(10px);
    }

    .feature-icon {
        font-size: 3rem;
        background: linear-gradient(135deg, #00ff88, #ffffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }

    .feature-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 1rem;
    }

    .feature-description {
        color: #b8b8d4;
        font-size: 1rem;
    }

    .stat-item {
        text-align: center;
        padding: 1rem;
    }

    .stat-number {
        font-size: 3rem;
        font-weight: 700;
        color: #00ff88;
        text-shadow: 0 0 20px rgba(0,255,136,0.5);
    }

    .stat-label {
        font-size: 1.1rem;
        color: #b8b8d4;
    }
</style>
""", unsafe_allow_html=True)

# Hero Section with hover highlight and new name
st.markdown("""
<div class="hero-section">
    <div class="hero-title">TRADING GUIDE APP</div>
    <div class="hero-subtitle">Professional Trading & Investment Platform</div>
    <p style="color: #9999b3; font-size: 1.1rem; max-width: 650px; margin: 0 auto;">
        Unlock the power of advanced trading analytics, real-time market insights, and AI-driven investment strategies. 
        Your gateway to professional-grade financial tools.
    </p>
</div>
""", unsafe_allow_html=True)

# Stats Section
st.markdown("""
<div class="stats-container">
    <div style="text-align: center; margin-bottom: 3rem;">
        <h2 style="color: #ffffff; font-size: 2.5rem;">Trusted by Traders Worldwide</h2>
        <p style="color: #b8b8d4; font-size: 1.2rem;">Join thousands of successful traders using our platform</p>
    </div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="stat-item">
        <div class="stat-number">$2.5B+</div>
        <div class="stat-label">Trading Volume</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-item">
        <div class="stat-number">50K+</div>
        <div class="stat-label">Active Traders</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-item">
        <div class="stat-number">99.9%</div>
        <div class="stat-label">Uptime</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="stat-item">
        <div class="stat-number">24/7</div>
        <div class="stat-label">Support</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Features Section
st.markdown("""
<div style="text-align: center; margin: 4rem 0 3rem;">
    <h2 style="color: #ffffff; font-size: 2.5rem;">Powerful Trading Tools</h2>
    <p style="color: #b8b8d4; font-size: 1.2rem;">Everything you need for successful trading in one platform</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <div class="feature-title">Advanced Analytics</div>
        <div class="feature-description">
            Technical indicators, real-time charts, and professional tools for deep market insight.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🤖</div>
        <div class="feature-title">AI-Powered Insights</div>
        <div class="feature-description">
            Machine learning models detect patterns and offer predictive signals.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">⚡</div>
        <div class="feature-title">Fast Execution</div>
        <div class="feature-description">
            Lightning-fast order placement and market updates in real-time.
        </div>
    </div>
    """, unsafe_allow_html=True)

# Navigation Section
st.markdown("""
<div style="text-align: center; margin: 4rem 0 2rem;">
    <h2 style="color: #ffffff; font-size: 2.5rem;">Trading Suite</h2>
    <p style="color: #b8b8d4; font-size: 1.2rem;">Explore core modules of our trading ecosystem</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="navigation-menu">
        <div class="menu-item">
            <div class="menu-title">📈 Trading Dashboard</div>
            <div class="menu-description">Real-time portfolio management and tracking</div>
        </div>
        <div class="menu-item">
            <div class="menu-title">📊 CAPM Beta Analysis</div>
            <div class="menu-description">Evaluate systematic risk with beta analysis</div>
        </div>
        <div class="menu-item">
            <div class="menu-title">💰 CAPM Return Calculator</div>
            <div class="menu-description">Predict stock returns using CAPM formula</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="navigation-menu">
        <div class="menu-item">
            <div class="menu-title">🔍 Stock Analysis</div>
            <div class="menu-description">Analyze stocks with advanced metrics</div>
        </div>
        <div class="menu-item">
            <div class="menu-title">🔮 Stock Prediction</div>
            <div class="menu-description">Forecast price using machine learning</div>
        </div>
        <div class="menu-item">
            <div class="menu-title">📱 Mobile Interface</div>
            <div class="menu-description">Optimized layout for mobile use</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; padding: 3rem 0; margin-top: 4rem; border-top: 1px solid rgba(0,255,136,0.2);">
    <p style="color: #666; font-size: 0.9rem;">
        © 2024 Trading Guide App. All rights reserved.
    </p>
    <p style="color: #888; font-size: 0.8rem; margin-top: 1rem;">
        ⚠️ Trading involves risk. Past performance does not guarantee future results.
    </p>
</div>
""", unsafe_allow_html=True)
