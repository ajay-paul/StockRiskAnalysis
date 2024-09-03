import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Conv1D, MaxPooling1D, Flatten
from tensorflow.keras.optimizers import Adam
from sklearn.preprocessing import MinMaxScaler
from transformers import BertTokenizer, TFBertModel
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Dense, LayerNormalization, MultiHeadAttention
import tensorflow as tf
from stable_baselines3 import DQN
from trading_env import StockTradingEnv
from .models import StockData, StockPrediction


def build_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=input_shape))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50))
    model.add(Dropout(0.2))
    model.add(Dense(units=1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def build_cnn_model(input_shape):
    model = Sequential()
    model.add(Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=input_shape))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Flatten())
    model.add(Dense(units=50, activation='relu'))
    model.add(Dense(units=1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def build_transformer_model(input_shape):
    inputs = Input(shape=input_shape)
    x = Dense(64, activation='relu')(inputs)
    x = LayerNormalization()(x)
    x = MultiHeadAttention(4, 16)(x, x)
    x = Dense(32, activation='relu')(x)
    x = Dense(1)(x)
    model = Model(inputs=inputs, outputs=x)
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def load_rl_model():
    return DQN.load('stock_trading_dqn_model')

# Use the RL model to make predictions
def predict_stock_trading_action(stock_data):
    model = load_rl_model()
    env = StockTradingEnv(stock_data)
    state = env.reset()
    action, _ = model.predict(state)
    return action

# Example function to integrate RL-based predictions
def integrate_rl_predictions(stock_symbol):
    data = StockData.objects.filter(symbol=stock_symbol).order_by('date')
    df = pd.DataFrame(list(data.values('open', 'high', 'low', 'close', 'volume')))
    action = predict_stock_trading_action(df)
    # Map action to trading decision
    if action == 0:
        decision = 'Buy'
    elif action == 1:
        decision = 'Hold'
    elif action == 2:
        decision = 'Sell'
    return decision

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

def train_cnn_model(stock_symbol):
    data = StockData.objects.filter(symbol=stock_symbol).order_by('date')
    features = np.array([[d.open, d.high, d.low, d.volume] for d in data])
    target = np.array([d.close for d in data])

    scaler = MinMaxScaler()
    features_scaled = scaler.fit_transform(features)
    target_scaled = scaler.fit_transform(target.reshape(-1, 1))

    features_scaled = np.reshape(features_scaled, (features_scaled.shape[0], features_scaled.shape[1], 1))

    model = build_cnn_model((features_scaled.shape[1], 1))
    model.fit(features_scaled, target_scaled, epochs=100, batch_size=32)

    return model, scaler

def train_transformer_model(stock_symbol):
    data = StockData.objects.filter(symbol=stock_symbol).order_by('date')
    features = np.array([[d.open, d.high, d.low, d.volume] for d in data])
    target = np.array([d.close for d in data])

    scaler = MinMaxScaler()
    features_scaled = scaler.fit_transform(features)
    target_scaled = scaler.fit_transform(target.reshape(-1, 1))

    model = build_transformer_model((features_scaled.shape[1],))
    model.fit(features_scaled, target_scaled, epochs=100, batch_size=32)

    return model, scaler

def load_rl_model():
    return DQN.load('stock_trading_dqn_model')

# Use the RL model to make predictions
def predict_stock_trading_action(stock_data):
    model = load_rl_model()
    env = StockTradingEnv(stock_data)
    state = env.reset()
    action, _ = model.predict(state)
    return action

# Example function to integrate RL-based predictions
def integrate_rl_predictions(stock_symbol):
    data = StockData.objects.filter(symbol=stock_symbol).order_by('date')
    df = pd.DataFrame(list(data.values('open', 'high', 'low', 'close', 'volume')))
    action = predict_stock_trading_action(df)
    # Map action to trading decision
    if action == 0:
        decision = 'Buy'
    elif action == 1:
        decision = 'Hold'
    elif action == 2:
        decision = 'Sell'
    return decision

def make_prediction(stock_symbol, model, scaler):
    latest_data = StockData.objects.filter(symbol=stock_symbol).order_by('-date')[:1]
    features = np.array([[d.open, d.high, d.low, d.volume] for d in latest_data])
    features_scaled = scaler.transform(features)
    
    if isinstance(model.input_shape, tuple) and len(model.input_shape) == 3:
        features_scaled = np.reshape(features_scaled, (features_scaled.shape[0], features_scaled.shape[1], 1))
    else:
        features_scaled = np.reshape(features_scaled, (features_scaled.shape[0], features_scaled.shape[1]))

    predicted_price = model.predict(features_scaled)
    predicted_price = scaler.inverse_transform(predicted_price)
    
    prediction = StockPrediction(stock=latest_data[0], predicted_price=predicted_price[0][0])
    prediction.save()
    
    return predicted_price[0][0]
