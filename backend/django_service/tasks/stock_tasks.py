import time
from celery import shared_task
from django_service.core.services import (
    predict_with_lstm,
    predict_with_transformer,
    optimize_strategy_with_rl,
)

@shared_task
def run_lstm_prediction(data):
    time.sleep(2)  # Simulate heavy computation
    prediction = predict_with_lstm(data)
    return {"model": "LSTM", "prediction": prediction}

@shared_task
def run_transformer_prediction(data):
    time.sleep(3)  # Simulate heavy computation
    prediction = predict_with_transformer(data)
    return {"model": "Transformer", "prediction": prediction}

@shared_task
def optimize_trading_strategy(data):
    time.sleep(5)  # Simulate heavy computation
    result = optimize_strategy_with_rl(data)
    return {"model": "RL", "optimized_strategy": result}
