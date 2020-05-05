import telebot
from telebot import apihelper
import requests
import json

# requests.packages.urllib3.disable_warnings()

# 本地测试需要代理
# apihelper.proxy = {
#     'http': 'http://127.0.0.1:1087', 
#     'https': 'http://127.0.0.1:1087'    
# }

API_TOKEN = None

with open('config/telegramcfg.json', 'r') as f:
    jsonObj = json.load(f)
    API_TOKEN = jsonObj['token']

bot = telebot.TeleBot(API_TOKEN)

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
""")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)

bot.polling()
