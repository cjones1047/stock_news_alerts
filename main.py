import os
from dotenv import load_dotenv
import requests

load_dotenv()

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
alphavantage_api_key = os.getenv("ALPHAVANTAGE_API_KEY")

alphavantage_parameters = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK,
    "apikey": alphavantage_api_key
}

response = requests.get("https://www.alphavantage.co/query", params=alphavantage_parameters)
response.raise_for_status()
alphavantage_days_data = response.json()["Time Series (Daily)"]
last_two_days = [kv_pair for i, kv_pair in enumerate(alphavantage_days_data.values()) if i < 2]
daily_price_change = float(last_two_days[0]["4. close"]) - float(last_two_days[1]["4. close"])
daily_price_change_percent = round(daily_price_change / float(last_two_days[1]["4. close"]) * 100, 1)
print(daily_price_change_percent)

# todays_date = datetime.date.today()
# yesterdays_date = todays_date - datetime.timedelta(days=1)
# print(yesterdays_date)

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

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

