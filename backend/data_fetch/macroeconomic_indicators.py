import requests

def fetch_macroeconomic_indicators(country_code="IN"):

    api_url = f"https://api.tradingeconomics.com/country/{country_code}/indicator/gdp?c=API_KEY"
    
    response = requests.get(api_url)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        
        # Extract and return the relevant macroeconomic indicators
        indicators = {
            'GDP': None,
            'Inflation': None,
            'Unemployment': None
        }
        
        for item in data:
            if item.get('category') == 'GDP Annual Growth Rate':
                indicators['GDP'] = item.get('value')
            elif item.get('category') == 'Inflation Rate':
                indicators['Inflation'] = item.get('value')
            elif item.get('category') == 'Unemployment Rate':
                indicators['Unemployment'] = item.get('value')

        return indicators
    
    # Return None in case of a failed request
    return None

def print_macroeconomic_indicators():
    indicators = fetch_macroeconomic_indicators()
    if indicators:
        print("Macroeconomic Indicators for India:")
        print(f"GDP: {indicators['GDP']}%")
        print(f"Inflation: {indicators['Inflation']}%")
        print(f"Unemployment: {indicators['Unemployment']}%")
    else:
        print("Failed to fetch macroeconomic data.")

# Example usage
# print_macroeconomic_indicators()
