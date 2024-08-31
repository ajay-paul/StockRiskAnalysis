from celery import shared_task
from .ml_model import train_lstm_model, make_prediction
from .models import StockData

@shared_task
def fetch_and_store_stock_data(symbol):
    # Fetch data from Kite API and store in the database
    pass

@shared_task
def train_model_task(symbol):
    model, scaler = train_lstm_model(symbol)
    return model, scaler

@shared_task
def predict_stock_price_task(symbol):
    model, scaler = train_model_task(symbol)
    predicted_price = make_prediction(symbol, model, scaler)
    return predicted_price
