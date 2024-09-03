import requests
from bs4 import BeautifulSoup
import datetime


API_KEY = "NEWS_API_KEY"  
def fetch_global_events(api_key):
    """
    Fetch global news articles using the News API.
    """
    api_url = f"https://newsapi.org/v2/top-headlines?category=world&apiKey={api_key}"
    response = requests.get(api_url)
    if response.status_code == 200:
        global_news = response.json()
        return global_news.get('articles', [])
    else:
        print("Failed to fetch global events.")
        return []

def fetch_global_events_from_web():
    """
    Fetch global events from a financial news website as an alternative to News API.
    """
    news_url = "https://www.moneycontrol.com/news/global"
    response = requests.get(news_url)
    if response.status_code != 200:
        print("Failed to fetch global events from the web.")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    news_articles = []
    
    for item in soup.find_all('div', class_='newsbox'):
        title = item.find('a').get_text(strip=True)
        link = item.find('a')['href']
        date = item.find('span', class_='date').get_text(strip=True) if item.find('span', class_='date') else 'No date'
        news_articles.append({'title': title, 'link': link, 'date': date})

    return news_articles

def print_global_events(api_key):
    """
    Fetch and print global events for stock market analysis.
    """
    news_from_api = fetch_global_events(api_key)
    news_from_web = fetch_global_events_from_web()

    if news_from_api:
        print("Global News (via API):")
        for article in news_from_api:
            print(f"Title: {article['title']}, Source: {article.get('source', {}).get('name', 'Unknown')}, URL: {article['url']}")
    
    if news_from_web:
        print("\nGlobal News (via Web Scraping):")
        for article in news_from_web:
            print(f"Title: {article['title']}, Date: {article['date']}, URL: {article['link']}")

# Example usage
# print_global_events(API_KEY)
