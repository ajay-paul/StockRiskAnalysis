# backend/stock/tasks.py

from .models import StockData, StockPrediction
from .ml_model import build_lstm_model, train_lstm_model, make_prediction
from kiteconnect import KiteConnect
from celery import shared_task
import redis

# Redis setup
r = redis.StrictRedis(host='localhost', port=6379, db=0)

# Kite API setup
KITE_API_KEY = "api_key"
KITE_ACCESS_TOKEN = "access_token"
kite = KiteConnect(api_key=KITE_API_KEY)
kite.set_access_token(KITE_ACCESS_TOKEN)

@shared_task
def fetch_and_store_live_data(stock_symbol):
    """Fetch live data using Kite API and store it in the StockData model."""
    try:
        live_data = kite.ltp(stock_symbol)
        stock_data = StockData(
            symbol=stock_symbol,
            open=live_data[stock_symbol]['last_price'],  
            high=live_data[stock_symbol]['last_price'],  
            low=live_data[stock_symbol]['last_price'], 
            volume=1000, 
            close=live_data[stock_symbol]['last_price']
        )
        stock_data.save()

        # Cache the data in Redis
        cache_key = f"live_data_{stock_symbol}"
        r.setex(cache_key, 3600, live_data)  # Cache data for 1 hour

        return stock_data
    except Exception as e:
        print(f"Error fetching live stock data: {e}")
        return None

@shared_task
def process_stock_data(stock_symbol):
    """Train the LSTM model and make predictions."""
    # Fetch live data first
    stock_data = fetch_and_store_live_data(stock_symbol)
    
    if stock_data:
        model, scaler = train_lstm_model(stock_symbol)

        predicted_price = make_prediction(stock_symbol, model, scaler)

        return predicted_price
    return None
