import time
from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch
import numpy as np
from django.contrib.auth.models import User
from .models import Watchlist

# Load the model and tokenizer
MODEL_NAME = "./Model/path"  # Replace with the actual model path
try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
except Exception as e:
    raise RuntimeError(f"Error loading model: {e}")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

text_pipeline = pipeline(
    "text-classification",
    model=model,
    tokenizer=tokenizer,
    device=0 if torch.cuda.is_available() else -1 
)

try:
    lstm_model = tf.keras.models.load_model("models/lstm_model.h5")  
except Exception as e:
    raise RuntimeError(f"Error loading LSTM model: {e}")


@shared_task
def run_lstm_prediction(data):
    """
    Perform LSTM-based stock prediction.
    """
    try:
        if not isinstance(data, dict) or "sequence" not in data:
            return {"error": "Invalid input. 'data' must include a 'sequence' field."}

        input_sequence = np.array(data["sequence"]).reshape(1, -1, 1)
        prediction = lstm_model.predict(input_sequence)

        return {"model": "LSTM", "prediction": prediction.tolist()}
    except Exception as e:
        return {"error": f"LSTM prediction failed: {e}"}


@shared_task
def run_transformer_prediction(data):
    """
    Perform Transformer-based stock prediction.
    """
    try:
        if not isinstance(data, dict) or "text" not in data:
            return {"error": "Invalid input. 'data' must include a 'text' field."}

        inputs = data["text"]
        prediction = text_pipeline(inputs)
        return {"model": "Transformer", "prediction": prediction}
    except Exception as e:
        return {"error": f"Transformer prediction failed: {e}"}


@shared_task
def predict_watchlist_and_notify(user_id):
    """
    Predict stock trends for user's watchlist and send notifications.
    """
    try:
        # Fetch the user's watchlist
        user = User.objects.get(id=user_id)
        watchlist = Watchlist.objects.filter(user=user)

        predictions = []
        for item in watchlist:
            # Perform predictions for each stock in the watchlist
            prediction = run_transformer_prediction({"text": item.stock_symbol}).get()
            predictions.append({"stock_symbol": item.stock_symbol, "prediction": prediction})

            # Send real-time notification for the prediction
            send_notification(
                f"Prediction for {item.stock_symbol}: {prediction['prediction']}"
            )

        return {"user": user.username, "predictions": predictions}
    except Exception as e:
        return {"error": f"Watchlist prediction failed: {e}"}


def send_notification(message):
    """
    Send real-time notifications to WebSocket group.
    """
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notifications",
        {
            "type": "send_notification",
            "message": message,
        }
    )
