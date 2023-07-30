import requests
import datetime as dt
from datetime import timedelta
from twilio.rest import Client
import os
Func = "TIME_SERIES_DAILY"
STOCK = "Cipla"

ALPHAVANTAGE_API = os.environ.get("ALPHAVANTAGE_API")
ACCOUNT_SID = os.environ.get("ACCOUNT_SID")
AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
NEWS_API = os.environ.get("NEWS_API")
client = Client(ACCOUNT_SID, AUTH_TOKEN)

now = dt.datetime.now()
if now.weekday() != 6:
    yesterday_date = str(now.date() - timedelta(days=1))
    day_before_yesterday_date = str(now.date() - timedelta(days=2))
else:
    yesterday_date = str(now.date() - timedelta(days=2))
    day_before_yesterday_date = str(now.date() - timedelta(days=3))


def get_news(percentage):
    news_response = requests.get(
        url=f"https://newsapi.org/v2/everything?q=cipla&apiKey={NEWS_API}")
    articles = news_response.json()["articles"]

    for article in articles[:3]:
        news_title = article["title"]
        news_description = article["description"]
        news = f"{STOCK}: {percentage}\nHeadline: " + news_title + "\nBrief: " + news_description
        message = client.messages.create(
            body=news,
            from_='+15392212437',
            to='+919098404515'
        )
        print(message.status)


stock_response = requests.get(
    url=f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={STOCK}.BSE&outputsize=full&apikey="
        f"{ALPHAVANTAGE_API}")
stock_yesterday = float(stock_response.json()["Time Series (Daily)"][yesterday_date]["4. close"])

stock_day_before_yesterday = float(stock_response.json()["Time Series (Daily)"][day_before_yesterday_date]["4. close"])

STOCK_PERCENTAGE = (stock_yesterday - stock_day_before_yesterday)/stock_yesterday * 100
if STOCK_PERCENTAGE > 1:
    get_news(f"▲ {STOCK_PERCENTAGE}%")
elif STOCK_PERCENTAGE < -1:
    get_news(f"🔻{abs(STOCK_PERCENTAGE)}%")
