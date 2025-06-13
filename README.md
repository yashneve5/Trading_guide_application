# Trading_guide_application
# 📈 Trading Guide App

**An all-in-one dashboard for stock analytics, CAPM evaluation, and AI-driven prediction tools.**

---

## 🚀 Overview

The **Trading Guide App** is a feature-rich **Streamlit** application designed for modern traders and investors. It integrates:

- **CAPM Beta & Return Calculator**: Quantify systematic risk and estimate expected returns.
- **Stock Analysis Dashboard**: Visualize historical data, technical indicators, and company fundamentals.
- **Stock Prediction Module**: Forecast future stock prices using time series models with intuitive reporting.

Under a **stylish, responsive UI**, this app lets users explore market data confidently without jumping between tools.

---

## 💻 Project Structure
Trading_guide_application:
  Home.py: "Main Streamlit entry point"
  pages:
    CAPM_Beta.py: "Calculates Beta using CAPM model"
    CAPM_Return.py: "Computes expected return using CAPM"
    STOCK_Analysis.py: "Technical indicators & stock charts"
    STOCK_Prediction.py: "Time series forecasting (ARIMA/LSTM)"
    utils:
      plotly_figure.py: "Plotting and chart utilities using Plotly"
      model_train.py: "Model training and data processing"
  README.md: "Documentation"
