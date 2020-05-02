import telebot
from telebot import apihelper
import requests
import json

requests.packages.urllib3.disable_warnings()

apihelper.proxy = {
    'http': 'http://127.0.0.1:1087', 
    'https': 'http://127.0.0.1:1087'    
}

def getBotToken():
    with open('config/telegramcfg.json', 'r') as f:
        jsonObj = json.load(f)
        return jsonObj['token']

def getChatId(token):
    url = 'https://api.telegram.org/bot{}/getUpdates'.format(token)
    resp = requests.get(url, proxies=apihelper.proxy, verify=False)
    jsonRetStr = resp.json()
    chatId = jsonRetStr['result'][0]['message']['from']['id']
    return str(chatId)

def pushGithubPocExpInfo(bot, chatId, pocExpInfo):
    pushTextMessage(bot, chatId, pocExpInfo) 

def pushTextMessage(bot, chatId, textMsg):
    bot.send_message(chatId, textMsg)
    
def runBot():
    token = getBotToken()
    bot = telebot.TeleBot(token)
    chatId = getChatId(token)
    bot.send_message(chatId, "hello, this is m01eBot!")
    pushTextMessage(bot, chatId, 'hello, this is m01eBot!')


if __name__ == '__main__':
    runBot()