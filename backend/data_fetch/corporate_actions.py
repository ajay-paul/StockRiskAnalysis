import requests
from bs4 import BeautifulSoup
import datetime

def fetch_corporate_actions_bse(stock_symbol):
    """
    Fetch recent corporate actions (like dividends, stock splits, etc.) 
    """

    bse_url = f"https://www.bseindia.com/corporates/corporate_act.aspx?scrip_cd={stock_symbol}&expandable=3"
    
    response = requests.get(bse_url)
    
    if response.status_code != 200:
        print(f"Failed to fetch corporate actions data for {stock_symbol}.")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    corporate_actions = []
    
    table = soup.find('table', {'class': 'table'})
    
    if table:
        rows = table.find_all('tr')[1:]  # Skipping the header row
        for row in rows:
            cols = row.find_all('td')
            if len(cols) > 1:
                action = {
                    'date': cols[0].get_text(strip=True),
                    'particulars': cols[1].get_text(strip=True),
                    'ex_date': cols[2].get_text(strip=True),
                    'purpose': cols[3].get_text(strip=True)
                }
                corporate_actions.append(action)
    
    return corporate_actions

def filter_recent_corporate_actions(corporate_actions, days=30):
    """
    Filter corporate actions within the last 'days' (default is 30 days).
    """
    recent_actions = []
    current_date = datetime.datetime.now()
    
    for action in corporate_actions:
        try:
            action_date = datetime.datetime.strptime(action['date'], '%d %b %Y')
            if (current_date - action_date).days <= days:
                recent_actions.append(action)
        except ValueError:
            continue  # Skip rows where date format is incorrect
    
    return recent_actions

def print_corporate_actions(stock_symbol):
    """
    Fetch and print corporate actions for the given stock symbol from BSE.
    """
    corporate_actions = fetch_corporate_actions_bse(stock_symbol)
    if corporate_actions:
        recent_actions = filter_recent_corporate_actions(corporate_actions)
        if recent_actions:
            print(f"Corporate Actions for {stock_symbol} in the last 30 days:")
            for action in recent_actions:
                print(f"Date: {action['date']}, Particulars: {action['particulars']}, Ex-Date: {action['ex_date']}, Purpose: {action['purpose']}")
        else:
            print(f"No recent corporate actions found for {stock_symbol}.")
    else:
        print(f"No corporate actions data available for {stock_symbol}.")

print_corporate_actions("TCS")
