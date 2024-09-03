import requests
from bs4 import BeautifulSoup
from transformers import pipeline
import re

def fetch_twitter_sentiments(stock_symbol):
    search_url = f"https://twitter.com/search?q={stock_symbol}&f=live"
    response = requests.get(search_url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        tweets = []
        
        for tweet in soup.find_all('div', {'data-testid': 'tweetText'}):
            text = tweet.get_text()
            tweets.append({'text': text})
        
        return tweets
    else:
        print(f"Failed to fetch Twitter data for {stock_symbol}.")
        return []

def fetch_reddit_sentiments(stock_symbol):
    search_url = f"https://www.reddit.com/r/stocks/search/?q={stock_symbol}&restrict_sr=1"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(search_url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        posts = []
        
        for post in soup.find_all('div', {'data-test-id': 'post-content'}):
            text = post.get_text()
            posts.append({'text': text})
        
        return posts
    else:
        print(f"Failed to fetch Reddit data for {stock_symbol}.")
        return []

def analyze_sentiments_with_transformers(sentiment_data):
    sentiment_analyzer = pipeline('sentiment-analysis')
    
    sentiment_scores = []
    for item in sentiment_data:
        result = sentiment_analyzer(item['text'])
        sentiment_scores.append(result[0]['label'])  # 'LABEL' could be 'POSITIVE', 'NEGATIVE', or 'NEUTRAL'
    
    return sentiment_scores

def calculate_herd_mentality(sentiment_scores):
    sentiment_scores_mapping = {
        'POSITIVE': 1,
        'NEGATIVE': -1,
        'NEUTRAL': 0
    }
    
    if not sentiment_scores:
        return None
    
    score_values = [sentiment_scores_mapping.get(score, 0) for score in sentiment_scores]
    average_score = sum(score_values) / len(score_values)
    
    # Normalize average sentiment score to a scale of 0-100
    herd_mentality_index = (average_score + 1) * 50  # Average score ranges from -1 to 1
    return round(herd_mentality_index, 2)

def fetch_herd_mentality(stock_symbol):
    """
    Fetch and calculate the herd mentality index for a given stock symbol.
    """
    twitter_data = fetch_twitter_sentiments(stock_symbol)
    reddit_data = fetch_reddit_sentiments(stock_symbol)
    
    all_sentiment_data = twitter_data + reddit_data
    sentiment_scores = analyze_sentiments_with_transformers(all_sentiment_data)
    herd_mentality_index = calculate_herd_mentality(sentiment_scores)
    
    return herd_mentality_index

# Example usage
stock_symbol = "TCS"  
herd_mentality_index = fetch_herd_mentality(stock_symbol)
print(f"Herd Mentality Index for {stock_symbol}: {herd_mentality_index}")
