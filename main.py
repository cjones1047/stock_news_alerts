import os
from dotenv import load_dotenv
import requests
import re
from twilio.rest import Client

load_dotenv()

STOCK = "TSLA"
COMPANY_NAME = "Tesla, Inc."

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
    msg_title = f"{STOCK}: 🔺 {daily_price_change_percent}%"
else:
    msg_title = f"{STOCK}: 🔻 {abs(daily_price_change_percent)}%"

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

twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_phone_num = os.getenv("TWILIO_PHONE_NUM")
recipient_phone_num = os.getenv("RECIPIENT_PHONE_NUM")

# Send a message with price change for chosen stock
client = Client(twilio_account_sid, twilio_auth_token)
message = client.messages.create(
    body=f"\n{msg_title}",
    from_=twilio_phone_num,
    to=recipient_phone_num
)

# Send a separate message with the percentage change and each article's title and description to you
for article in last_three_articles:
    old_description = article["description"]
    # remove all HTML tags from descriptions, including HTML entities not enclosed in carrots (<>)
    new_description = re.sub(re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});'), "", old_description)
    title = article["title"]

    message = client.messages.create(
        body=f"\nHeadline: {title}\n"
             f"\n- Brief: {new_description}",
        from_=twilio_phone_num,
        to=recipient_phone_num
    )
