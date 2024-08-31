from .models import StockData, StockPrediction
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import numpy as np

def build_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=input_shape))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50))
    model.add(Dropout(0.2))
    model.add(Dense(units=1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def train_lstm_model(stock_symbol):
    data = StockData.objects.filter(symbol=stock_symbol).order_by('date')
    features = np.array([[d.open, d.high, d.low, d.volume] for d in data])
    target = np.array([d.close for d in data])

    scaler = MinMaxScaler()
    features_scaled = scaler.fit_transform(features)
    target_scaled = scaler.fit_transform(target.reshape(-1, 1))

    features_scaled = np.reshape(features_scaled, (features_scaled.shape[0], 1, features_scaled.shape[1]))

    model = build_lstm_model((1, features_scaled.shape[2]))
    model.fit(features_scaled, target_scaled, epochs=100, batch_size=32)
    
    return model, scaler

def make_prediction(stock_symbol, model, scaler):
    latest_data = StockData.objects.filter(symbol=stock_symbol).order_by('-date')[:1]
    features = np.array([[d.open, d.high, d.low, d.volume] for d in latest_data])
    features_scaled = scaler.transform(features)
    features_scaled = np.reshape(features_scaled, (features_scaled.shape[0], 1, features_scaled.shape[1]))
    
    predicted_price = model.predict(features_scaled)
    predicted_price = scaler.inverse_transform(predicted_price)
    
    prediction = StockPrediction(stock=latest_data[0], predicted_price=predicted_price[0][0])
    prediction.save()
    
    return predicted_price[0][0]
