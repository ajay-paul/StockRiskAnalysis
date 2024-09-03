# trading_env.py
import gym
from gym import spaces
import numpy as np

class StockTradingEnv(gym.Env):
    def __init__(self, data):
        super(StockTradingEnv, self).__init__()
        self.data = data
        self.current_step = 0

        # Define action space: Buy (0), Hold (1), Sell (2)
        self.action_space = spaces.Discrete(3)
        # Define observation space: Stock prices and other features
        self.observation_space = spaces.Box(low=0, high=np.inf, shape=(len(data.columns),), dtype=np.float32)

    def reset(self):
        self.current_step = 0
        return self.data.iloc[self.current_step].values

    def step(self, action):
        self.current_step += 1
        done = self.current_step >= len(self.data) - 1
        reward = 0
        
        if action == 0:  # Buy
            reward = self.data['close'].iloc[self.current_step + 1] - self.data['close'].iloc[self.current_step]
        elif action == 1:  # Hold
            reward = 0
        elif action == 2:  # Sell
            reward = self.data['close'].iloc[self.current_step] - self.data['close'].iloc[self.current_step + 1]
        
        next_state = self.data.iloc[self.current_step].values
        return next_state, reward, done, {}
