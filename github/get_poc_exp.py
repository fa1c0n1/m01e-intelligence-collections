import requests
import json
import os
import datetime
from github import Github
from telebot import apihelper
from telebot import util
import telebot
import time

'''
脚本用途：
该脚本用来监控github上的cve漏洞的poc或exp,
并把结果通过Telegram Bot进行推送到自己的telegram账号
'''

requests.packages.urllib3.disable_warnings()

# 本地测试的时候，需要通过代理访问
# apihelper.proxy = {
#     'http': 'http://127.0.0.1:1087', 
#     'https': 'http://127.0.0.1:1087'    
# }

# 可能以后会有多个关键词的需求，
#  后面可能还会配合多个搜索限定词，故这里使用列表
g_keyWords = [
    {
        "keyword": "cve-{}".format(datetime.datetime.now().year),
        "total_count": 0
    },
]

def getGithubObject():
    with open('config/githubcfg.json', 'r') as f:
        jsonObj = json.load(f)
        accessToken = jsonObj['access_token']
        g = Github(accessToken) 
        return g

def searchRepo(gtbObj, keyword, sort='stars'):
    repos = gtbObj.search_repositories(query=keyword, sort=sort)
    return repos
    

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

def pushGithubPocExpInfo(bot, chatId, pocExpInfos):
    pushTextMessage(bot, chatId, pocExpInfos) 

def pushTextMessage(bot, chatId, textMsg):
    bot.send_message(chatId, textMsg)

def monitorPocOrExp(gtbObj):
    repos = None
    if g_keyWords[0]['total_count'] == 0:
        repos = searchRepo(gtbObj, keyword=g_keyWords[0]['keyword'], sort='stars')
    else:
        repos = searchRepo(gtbObj, keyword=g_keyWords[0]['keyword'], sort='updated')
    return repos

    
def scriptRun():
    token = getBotToken()
    bot = telebot.TeleBot(token)
    chatId = getChatId(token)
    githubObj = getGithubObject()

    print("启动github监控...")

    # 轮询监控
    while True:
        print('github监控中...')
        repos = monitorPocOrExp(githubObj)
        if repos.totalCount > g_keyWords[0]['total_count']:
            newCount = repos.totalCount - g_keyWords[0]['total_count']
            pocExpInfos = ''
            for i in range(newCount):
                pocExpInfo = '【{}】{}\n描述：{}\n{}\n' \
                    .format(i+1, repos[i].full_name, repos[i].description, repos[i].html_url)
                pocExpInfos += pocExpInfo
    
                if (i + 1) % 10 == 0:
                    # 分批推送到telegram
                    pushGithubPocExpInfo(bot, chatId, pocExpInfos)
                    pocExpInfos = ''
            
            # newCount不是10的倍数的情况
            if pocExpInfos != '':
                pushGithubPocExpInfo(bot, chatId, pocExpInfos)
                pocExpInfos = ''
                
            g_keyWords[0]['total_count'] = repos.totalCount

        # 等待5分钟
        time.sleep(5*60)


if __name__ == '__main__':
    scriptRun()

