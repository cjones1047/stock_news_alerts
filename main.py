import os
from dotenv import load_dotenv
import requests
import re

load_dotenv()

STOCK = "TSLA"
COMPANY_NAME = "Tesla, Inc."

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
alphavantage_api_key = os.getenv("ALPHAVANTAGE_API_KEY")

alphavantage_parameters = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK,
    "apikey": alphavantage_api_key
}

alphavantage_response = requests.get("https://www.alphavantage.co/query", params=alphavantage_parameters)
alphavantage_response.raise_for_status()
alphavantage_days_data = alphavantage_response.json()["Time Series (Daily)"]
last_two_days = [kv_pair for i, kv_pair in enumerate(alphavantage_days_data.values()) if i < 2]
daily_price_change = float(last_two_days[0]["4. close"]) - float(last_two_days[1]["4. close"])
daily_price_change_percent = round(daily_price_change / float(last_two_days[1]["4. close"]) * 100, 1)

if daily_price_change_percent > 0:
    title = f"{STOCK}: 🔺 {daily_price_change_percent}%"
else:
    title = f"{STOCK}: 🔻 {abs(daily_price_change_percent)}%"

print(title)

newsapi_api_key = os.getenv("NEWSAPI_API_KEY")

newsapi_parameters = {
    "q": COMPANY_NAME,
    "from": list(alphavantage_days_data.keys())[1],
    "sortBy": "popularity",
    "language": "en",
    "apiKey": newsapi_api_key
}

newsapi_response = requests.get("https://newsapi.org/v2/everything", params=newsapi_parameters)
newsapi_response.raise_for_status()
last_three_articles = newsapi_response.json()["articles"][:3]
for article in last_three_articles:
    old_description = article["description"]
    # remove all HTML tags from descriptions, including HTML entities not enclosed in carrots (<>)
    new_description = re.sub(re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});'), "", old_description)
    article["description"] = new_description

print(last_three_articles)

## STEP 3: Use https://www.twilio.com
# Send a separate message with the percentage change and each article's title and description to your phone number.


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

