from flask import Flask, request
import json
from flask_sslify import SSLify
import telebot
import requests
import mysql.connector


app = Flask(__name__)
sslify = SSLify

bot = telebot.TeleBot("")

if __name__ == "__main__":
    app.run()

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        name = r['message']['chat']['first_name']
        chat_id = r['message']['chat']['id']
        message = r['message']['text']
        message = message.lower()

        connection = mysql.connector.connect(user="", password="",
                                             host="",
                                             database="")
        cursor = connection.cursor(buffered=True)

        return "POST request оброблений успішно"
    else:
        return "GET request оброблений успішно"

def priority(message, cursor):
    cursor.execute("SELECT question FROM base")
    rows = cursor.fetchall()
    pr_list = []
    maximum = 0

    for x in rows:
        prior = 1
        x = x[0].lower()
        question = x.split(" ")
        for i in question:
            for i in message:
                prior = prior + 1
        pr_list.append(prior)

    for c in pr_list:
        if c > maximum:
            maximum = c
    position = pr_list.index(maximum)

    for z in rows:
        if rows.index(z) == position:
            if maximum > 1:
                return z[0]
            else:
                return 0

front = telebot.types.ReplyKeyboardMarkup(True, False)
front.row('Новини', 'Курс валют')

news = telebot.types.ReplyKeyboardMarkup(True, False)
news.row('business', 'health', 'entertainment')
news.row('science', 'sports', 'technology')
news.row('Назад')

exchange_rates = telebot.types.ReplyKeyboardMarkup(True, False)
exchange_rates.row('EUR', 'UAN', 'USD')
exchange_rates.row('Назад')

def parse_exchange():
    bank_api = json.loads(requests.get('https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5'))
    return bank_api

def parse_news(chat_id, category):
    news_api = json.loads(requests.get('https://newsapi.org/v2/top-headlines?country=' + category + '&apiKey=98b32d9786f54ca49637a937542b8901').text)

    articles = news_api['articles']
    for article in articles[:3]:
        title = article['title']
        source = article['url']
        text = article['description']
        bot.send_message(chat_id, title + '\n\n' + text + '\n\n' + 'джерело: ' + source)

