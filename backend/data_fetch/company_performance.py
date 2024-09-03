import requests
from bs4 import BeautifulSoup
import tweepy
import json

# Twitter API setup 
twitter_api_key = 'TWITTER_API_KEY'
twitter_api_secret = 'TWITTER_API_SECRET'
twitter_access_token = 'TWITTER_ACCESS_TOKEN'
twitter_access_token_secret = 'TWITTER_ACCESS_TOKEN_SECRET'

def setup_twitter_api():
    auth = tweepy.OAuth1UserHandler(
        twitter_api_key, twitter_api_secret,
        twitter_access_token, twitter_access_token_secret
    )
    return tweepy.API(auth)

def fetch_twitter_data(stock_symbol):
    api = setup_twitter_api()
    query = f"{stock_symbol} BSE"
    tweets = api.search(q=query, lang="en", count=5)  # Adjust the count as needed

    tweet_data = []
    for tweet in tweets:
        tweet_data.append({
            'user': tweet.user.screen_name,
            'text': tweet.text,
            'created_at': tweet.created_at
        })
    
    return tweet_data

def fetch_web_data(stock_symbol):
    # Example of web scraping news from a financial news site
    search_url = f"https://www.moneycontrol.com/news/search/news/{stock_symbol}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    news_articles = []
    for item in soup.find_all('a', class_='newsitem'):
        title = item.get_text()
        link = item['href']
        news_articles.append({'title': title, 'link': link})
    
    return news_articles

def print_web_data(stock_symbol):
    # Fetching the web data
    news_data = fetch_web_data(stock_symbol)
    
    # Printing the fetched news data
    if news_data:
        print(f"News for {stock_symbol}:")
        for article in news_data:
            print(f"Title: {article['title']}")
            print(f"Link: {article['link']}")
            print("-" * 80)  # Separator for readability
    else:
        print(f"No news articles found for {stock_symbol}.")
        news_data_available = 0

# Example usage
# print_web_data('TCS')


def fetch_company_performance(stock_symbol):
    # API for company financials
    news_url = f"https://newsapi.org/v2/everything?q={stock_symbol}+BSE&apiKey=YOUR_NEWS_API_KEY"
    reports_url = f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={stock_symbol}.BSE&apikey=YOUR_API_KEY"

    # Fetch data from APIs
    news_response = requests.get(news_url)
    reports_response = requests.get(reports_url)
    news_data = news_response.json()
    reports_data = reports_response.json()

    # Fetch data from Twitter and web scraping
    twitter_data = fetch_twitter_data(stock_symbol)
    web_data = fetch_web_data(stock_symbol)

    performance = {
        "news": news_data.get('articles', []),
        "financial_reports": reports_data.get('annualReports', []),
        "twitter": twitter_data,
        "web_data": web_data
    }
    
    return performance

# Example usage for TCS on BSE
performance_data = fetch_company_performance('TCS')
print(json.dumps(performance_data, indent=4))
