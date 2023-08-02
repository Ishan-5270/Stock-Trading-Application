import requests
from twilio.rest import Client
import os 

stock = "GOOGL"
company_name = "Google"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
FUNCTION_NAME = "TIME_SERIES_INTRADAY"
STOCK_API_KEY = os.environ.get("STOCK_KEY")
NEWS_API_KEY = os.environ.get("NEWS_KEY")
account_sid = "AC7fabf305dbb69aaa81ef45635f18aefb"
auth_token = os.environ.get("AUTH_TOKEN")

STOCK_PARAMETERS = {
    "function": "TIME_SERIES_DAILY",
    "symbol": stock,
    "apikey": STOCK_API_KEY
}

NEWS_PARAMETERS = {
    "apiKey": NEWS_API_KEY,
    "q": f"{company_name} AND ({company_name} Stock)",
    "searchIn": "title"
}

response = requests.get(url=STOCK_ENDPOINT, params=STOCK_PARAMETERS)
data = response.json()
data = data["Time Series (Daily)"]
data_list = [_ for _ in data]

# Get yesterday and day before yesterdays stock price for the company
yesterdays_closing_price = data[f"{data_list[0]}"]["4. close"]
day_before_yest_closing = data[f"{data_list[1]}"]["4. close"]
percentage_change = (((float(yesterdays_closing_price) - float(day_before_yest_closing))/ float(day_before_yest_closing))*100)

if percentage_change > 0:
    rate = "🔼"
else:
    rate = "🔽"

if abs(percentage_change) > 3:

    news_response = requests.get(url=NEWS_ENDPOINT, params=NEWS_PARAMETERS)
    data = news_response.json()
    relevant_news = data["articles"]
    articles = relevant_news[:3]
    # slices the first 3 articles 

    formatted_article_list = [f"{stock}: {rate} {percentage_change} Headline: {article['title']}\nDescription: {article['description']}\nLink to the article: {article['url']}" 
                    for article in articles]

    client = Client(account_sid, auth_token)

    for article in formatted_article_list:
        message = client.messages \
                    .create(
                        body=article,
                        from_='+13642047422',
                        to='+919819147217'
                    )
        print(message.status)

