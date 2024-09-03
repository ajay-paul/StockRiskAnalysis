import yfinance as yf

def fetch_closing_prices(stock_symbol):
    """
    Fetches the most recent and previous closing prices for a given stock.
    """
    try:
        # Fetch historical data for the stock from Yahoo Finance
        stock = yf.Ticker(stock_symbol)
        hist = stock.history(period="5d")  # Fetch data for the last 5 days
        
        if len(hist) >= 2:
            # Use 'Close' price for the most recent two days
            recent_close = hist['Close'].iloc[-1]
            previous_close = hist['Close'].iloc[-2]
            return recent_close, previous_close
        else:
            return None, None
    except Exception as e:
        print(f"Error fetching data for {stock_symbol}: {e}")
        return None, None

def check_price_movement(stock_symbol):
    """
    Checks if the closing value for the stock has gone up or down and prints with color.
    """
    recent_close, previous_close = fetch_closing_prices(stock_symbol)
    if recent_close is not None and previous_close is not None:
        if recent_close > previous_close:
            movement = "up"
            color_code = "\033[92m"  # Green
        elif recent_close < previous_close:
            movement = "down"
            color_code = "\033[91m"  # Red
        else:
            movement = "no change"
            color_code = "\033[0m"   # No color (default)

        # Reset color to default
        reset_code = "\033[0m"

        print(f"Latest close price for {stock_symbol}: {recent_close:.2f}")
        print(f"Previous close price for {stock_symbol}: {previous_close:.2f}")
        print(f"{color_code}Closing value is {movement}.{reset_code}")
    else:
        print(f"Failed to fetch data for {stock_symbol}")

# List of stock symbols
stock_symbols = ["INFIBEAM.BO", "TCS.BO"]

# Check and display price movement for each stock symbol
for stock_symbol in stock_symbols:
    check_price_movement(stock_symbol)
