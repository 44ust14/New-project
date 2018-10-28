# import sys
import time
# import threading
# import random
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
# from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
# from telepot.namedtuple import InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent
import requests
from bs4 import BeautifulSoup
import bs4, requests
import json
from opencage.geocoder import OpenCageGeocode
import sqlite3
# conn = sqlite3.connect('sqlite:///E:\\New projectsss\\New-project\\main_db.db')
conn = sqlite3.connect('main_db.db')
cur = conn.cursor()

key = 'a279f5ab7cc1464da34cec0183dde7a0'
geocoder = OpenCageGeocode(key)

query = "Lviv"
result = geocoder.geocode(query)
if result and len(result):
        longitude = result[0]['geometry']['lng']
        latitude  = result[0]["geometry"]["lat"]
print(longitude,latitude)

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(msg)
    # response = requests.get('127.0.0.1:8001/person/{}'.format(msg['from']['id']))
    # update['message']['chat']['first_name']
    if content_type != 'text':
        bot.sendMessage(chat_id, "*Sorry, i understand only text messages😢*", parse_mode='Markdown')
        return
    command = msg['text']
    app_id = "f996f51b"
    app_key = "cdfb503fe8f18fe3784de8cdabf67581"


    if command == '/start' :
            markup = ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text='Current Weather')],
        [KeyboardButton(text='Week Weather')]
            ])
            # bot.sendMessage(chat_id, "", parse_mode='HTML')
            bot.sendMessage(chat_id, '*Hi*', reply_markup=markup, parse_mode='Markdown')
    conn = sqlite3.connect('main_db.db')
    cur = conn.cursor()
    # cur.execute("SELECT EXISTS(SELECT * FROM commands WHERE user_id=msg['from']['id'])")
    cur.execute("SELECT EXISTS(SELECT user_id FROM commands WHERE user_id=462005869)")
    result = cur.fetchall()
    print(result)
    if result == [(1,)]:
        print(command)
        query=command
        result = geocoder.geocode(query)
        # longitude = result[0]['geometry']['lng']
        # latitude  = result[0]["geometry"]["lat"]
        # com_sql = "DELETE FROM commands WHERE user_id= 462005869 "
        # cur.execute(com_sql)
        conn = sqlite3.connect('main_db.db')
        # cur = conn.cursor()
        # com_sql = "DELETE FROM commands WHERE user_id= 462005869 "
        # cur.execute(com_sql)
        # conn.commit()
        sql = 'DELETE FROM commands WHERE user_id=?'
        cur = conn.cursor()
        cur.execute(sql, (msg['from']['id'],))
        conn.commit()
        bot.sendMessage(chat_id,command)
    if result ==[(0,)]:

        bot.sendMessage(chat_id,"test no location")
    if command =='Current Weather':
        conn = sqlite3.connect('main_db.db')
        cur = conn.cursor()
        com_sql = "INSERT OR REPLACE INTO commands (user_id, location) VALUES (?, ?)"
        cur.execute(com_sql, (msg['from']['id'], '1'))
        conn.commit()
        bot.sendMessage(chat_id, 'Write your location')

    # if geocoder.geocode(command)!=False:
    #     query = command;
    #     result = geocoder.geocode(query)
    #     latitude  = result[0]["geometry"]["lat"]
    #     bot.sendMessage(chat_id,longitude,latitude)
        # http://api.weatherunlocked.com/api/trigger/49.841952,24.0315921/current temperature gt 16 includecurrent?app_id=f996f51b&app_key=cdfb503fe8f18fe3784de8cdabf67581
    # http://api.weatherunlocked.com/api/trigger/51.50,-0.12/forecast tomorrow temperature gt 16 include7dayforecast?app_id=f996f51b&app_key=cdfb503fe8f18fe3784de8cdabf67581
TOKEN = "754377431:AAFpoOOFXDcGZAliRTHja9UhnQYlvIZ4onQ"
bot = telepot.Bot(TOKEN)
answerer = telepot.helper.Answerer(bot)
try:
    MessageLoop(bot, {'chat': on_chat_message}).run_as_thread()
except:
    print('error')

print('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)
