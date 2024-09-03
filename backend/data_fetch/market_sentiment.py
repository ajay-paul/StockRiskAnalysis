import requests
import tweepy
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from transformers import pipeline

# Twitter API credentials (replace with your keys)
API_KEY = "TWITTER_API_KEY"
API_SECRET = "TWITTER_API_SECRET"
ACCESS_TOKEN = "TWITTER_ACCESS_TOKEN"
ACCESS_TOKEN_SECRET = "TWITTER_ACCESS_TOKEN_SECRET"

# HuggingFace Sentiment Analysis pipeline using transformers
sentiment_analyzer = pipeline("sentiment-analysis")


TIME_DELTA = timedelta(hours=48)

def authenticate_twitter_api():
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api

def is_recent_tweet(tweet_time):
    """Check if the tweet is within the recent time delta."""
    tweet_datetime = datetime.strptime(tweet_time, '%a %b %d %H:%M:%S +0000 %Y')
    current_time = datetime.utcnow()
    return current_time - tweet_datetime <= TIME_DELTA

def fetch_twitter_sentiment(stock_symbol):
    api = authenticate_twitter_api()
    
    # Define search query for Twitter
    query = f"{stock_symbol} stock"
    
    tweets = api.search_tweets(q=query, lang="en", count=100)
    
    if not tweets:
        return None
    
    positive, neutral, negative = 0, 0, 0
    
    # Analyze sentiment for each recent tweet using transformers
    for tweet in tweets:
        if is_recent_tweet(tweet.created_at):
            analysis = sentiment_analyzer(tweet.text)[0]  # Use transformers for sentiment analysis
            if analysis['label'] == "POSITIVE":
                positive += 1
            elif analysis['label'] == "NEUTRAL":
                neutral += 1
            else:
                negative += 1
    
    total = positive + neutral + negative
    if total == 0:
        return None  # No recent sentiment data found
    
    sentiment = {
        'positive': round(positive / total * 100, 2),
        'neutral': round(neutral / total * 100, 2),
        'negative': round(negative / total * 100, 2)
    }
    
    return sentiment

def fetch_news_sentiment(stock_symbol):
    news_url = f"https://www.moneycontrol.com/news/search/news/{stock_symbol}"
    response = requests.get(news_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    news_articles = []
    for item in soup.find_all('a', class_='newsitem'):
        title = item.get_text()
        link = item['href']
        news_articles.append({'title': title, 'link': link})
    
    positive, neutral, negative = 0, 0, 0
    
    for article in news_articles:
        # Analyze sentiment of the news title using transformers
        analysis = sentiment_analyzer(article['title'])[0]
        if analysis['label'] == "POSITIVE":
            positive += 1
        elif analysis['label'] == "NEUTRAL":
            neutral += 1
        else:
            negative += 1
    
    total = positive + neutral + negative
    if total == 0:
        return None
    
    sentiment = {
        'positive': round(positive / total * 100, 2),
        'neutral': round(neutral / total * 100, 2),
        'negative': round(negative / total * 100, 2)
    }
    
    return sentiment

def print_market_sentiment(stock_symbol):
    twitter_sentiment = fetch_twitter_sentiment(stock_symbol)
    news_sentiment = fetch_news_sentiment(stock_symbol)
    
    if twitter_sentiment:
        print(f"Twitter Sentiment for {stock_symbol}:")
        print(f"Positive: {twitter_sentiment['positive']}%")
        print(f"Neutral: {twitter_sentiment['neutral']}%")
        print(f"Negative: {twitter_sentiment['negative']}%")
    else:
        print(f"No recent sentiment data found on Twitter for {stock_symbol}.")
    
    if news_sentiment:
        print(f"News Sentiment for {stock_symbol}:")
        print(f"Positive: {news_sentiment['positive']}%")
        print(f"Neutral: {news_sentiment['neutral']}%")
        print(f"Negative: {news_sentiment['negative']}%")
    else:
        print(f"No sentiment data found from news sources for {stock_symbol}.")

# Example usage for TCS stock on BSE
# print_market_sentiment("TCS")
