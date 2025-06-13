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
Trading_guide_application/
│
- Home.py # 🚀 Streamlit entry point
- pages/
-│ ├── CAPM_Beta.py # 📊 Calculates Beta using CAPM
-│ ├── CAPM_Return.py # 💰 Computes expected return (CAPM)
-│ ├── STOCK_Analysis.py # 📈 Technical indicators (RSI, MACD, SMA)
-│ └── STOCK_Prediction.py # 🔮 Forecasting (ARIMA / LSTM)
-│
-├── pages/utils/
-│ ├── plotly_figure.py # 📉 Chart utilities using Plotly
-│ └── model_train.py # 🧠 Data preprocessing & model training
-│
-└── README.md # 📘 Project documentation

---

## 📌 Features

### 📈 CAPM Analysis
- **Beta Calculator** using regression with S&P 500.
- **Expected Return Calculator** using:
  \[
  E(R_i) = R_f + \beta (E(R_m) - R_f)
  \]

### 🧮 Stock Analytics
- Candlestick chart
- Moving Averages (SMA)
- Relative Strength Index (RSI)
- MACD with histogram and signal line
- Company info and key financials

### 🔮 Stock Price Prediction
- Uses historical data and models like ARIMA or LSTM.
- 30-day prediction with:
  - Forecast table
  - Line chart
  - RMSE evaluation

---

## ⚙️ How to Run

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/Trading_guide_application.git
cd Trading_guide_application
