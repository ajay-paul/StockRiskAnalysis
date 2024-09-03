# Stock Risk Analysis Project

This project implements a deep learning approach to stock prediction for the Indian stock market by leveraging multiple data sources such as historical stock prices, macroeconomic indicators, news sentiment, corporate actions, and global events. The goal is to develop models using LSTM, CNN, transformers, and reinforcement learning to predict stock movements and make informed trading decisions.

## Table of Contents

- [Introduction](#introduction)
- [Data Collection](#data-collection)
- [Preprocessing and Feature Engineering](#preprocessing-and-feature-engineering)
- [Model Architectures](#model-architectures)
  - [LSTM Model](#lstm-model)
  - [CNN Model](#cnn-model)
  - [Transformer Model](#transformer-model)
  - [Reinforcement Learning Model](#reinforcement-learning-model)
  - [Tech Stack](#tech-stack)
- [Evaluation](#evaluation)


## Introduction

Stock price prediction is a challenging task due to the complexity and volatility of the financial markets. In this project, we aim to develop robust deep learning models that take into account various factors such as supply and demand, company performance, macroeconomic indicators, market sentiment, corporate actions, global events, and herd mentality. We will experiment with models like Long Short-Term Memory (LSTM), Convolutional Neural Networks (CNN), transformers, and Reinforcement Learning (RL) techniques.

## Data Collection

We collect data from various sources to build a rich dataset for training and testing the models:

- **Supply and Demand**: Scraped from websites such as NSE India, BSE India, and Yahoo Finance for historical stock prices, volumes, and order book data.
- **Company Performance**: News articles, company reports, and earnings calls scraped using APIs like NewsAPI and parsed with `BeautifulSoup`.
- **Macroeconomic Indicators**: Data from sources like RBI, Ministry of Finance, IMF, and World Bank, including GDP, inflation, and interest rates.
- **Market Sentiment**: Collected from social media platforms such as Twitter and Reddit using APIs, and sentiment analysis performed using NLP models like `VADER` and `BERT`.
- **Corporate Actions**: Information on dividends, stock splits, mergers, and acquisitions obtained through stock exchange filings.
- **Global Events**: Scraped news articles related to global events, economic crises, and geopolitical tensions using APIs or web scraping.
- **Herd Mentality**: Analyzed through spikes in trading volumes and social media sentiment trends.

## Preprocessing and Feature Engineering

Once the data is collected, it undergoes preprocessing and feature engineering:

- **Normalization**: Scaling of stock prices and macroeconomic indicators using `MinMaxScaler` or `StandardScaler`.
- **NLP**: Text data from news articles and social media is processed using tokenization, sentiment scoring, and feature extraction.
- **Feature Engineering**: Lagged features, rolling averages, and sentiment scores are created for use in time-series models.

## Model Architectures

We implement and experiment with several deep learning and reinforcement learning models:

### LSTM Model

Long Short-Term Memory (LSTM) networks are ideal for capturing long-term dependencies in sequential data like stock prices and technical indicators.

### CNN Model
Convolutional Neural Networks (CNN) are effective at capturing local patterns in stock price movements and technical indicators.

### Transformer Model
Transformer models are used to capture long-term dependencies in the data by utilizing attention mechanisms. They are especially useful for combining text data (such as news) with numerical data.

### Reinforcement Learning Model
Reinforcement Learning (RL) models are used to develop trading strategies that optimize portfolio returns by learning to make buy/sell/hold decisions.

### Tech Stack

- **Backend:** Django, Python, Redis, PostgreSQL
- **Frontend:** React.js
- **Machine Learning:** LSTM, CNN, Transformers, Reinforcement Learning
- **Other Services:** Celery, Docker, Twilio, Zerodha Kite API


## Evaluation

We evaluate the models using backtesting on historical stock data:

- **Metrics**: Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), Sharpe Ratio, cumulative returns.
- **Backtesting**: Simulate how the model would have performed using past market data to test the robustness of predictions.
- **Live Testing**: Deploy models in a live trading environment with paper trading to evaluate their real-time performance.

## Installation

To install the necessary dependencies, run:

```bash
pip install -r requirements.txt

Ensure that you have Python 3.7+ and the following major dependencies:

- `Keras`
- `TensorFlow`
- `Transformers`
- `Stable-Baselines3`
- `KiteConnect`
- `BeautifulSoup4`
- `Selenium`
- `yfinance`
- `scikit-learn`
- `matplotlib`
