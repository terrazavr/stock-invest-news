import requests
import os
from dotenv import load_dotenv
import telebot

load_dotenv()


class APIRequests:
    def __init__(self):
        self.stock_endpoint = "https://www.alphavantage.co/query"
        self.news_endpoint = "https://newsapi.org/v2/everything"

    def stock_info(self, share_name):
        api_key = os.getenv("STOCK_API_KEY")
        stock_params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": share_name,
            "outputsize": "compact",
            "datatype": "json",
            "apikey": api_key,
        }
        stock_response = requests.get(self.stock_endpoint, params=stock_params)
        stock_response.raise_for_status()
        return stock_response.json()["Time Series (Daily)"]

    def check_news(self, company_name, language):
        api_key = os.getenv("NEWS_API_KEY")
        news_params = {
            "q": company_name,
            "sortBy": "relevancy",
            "language": language,
            "apiKey": api_key,
        }
        news_response = requests.get(self.news_endpoint, params=news_params)
        news_response.raise_for_status()
        news_data = news_response.json()
        articles_all = news_data["articles"]
        main_articles = [article for article in articles_all[:3]
                         if company_name in article["title"]
                         or company_name in article["description"]
                         ]
        return main_articles

    def telegram_message(self, message):
        token = os.getenv("TELEGRAMM_TOKEN")
        bot = telebot.TeleBot(token)
        chat_id = os.getenv("TELEGRAM_CHAT_ID")
        text = message
        return bot.send_message(chat_id, text)
