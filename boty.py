# import sys
import time
# import threading
# import random
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
import requests
from opencage.geocoder import OpenCageGeocode
import sqlite3
import urllib3
# conn = sqlite3.connect('sqlite:///E:\\New projectsss\\New-project\\main_db.db')
conn = sqlite3.connect('main_db.db')
cur = conn.cursor()

key = 'a279f5ab7cc1464da34cec0183dde7a0'
geocoder = OpenCageGeocode(key)
# query = "Lviv"
# result = geocoder.geocode(query)
# if result and len(result):
#         longitude = result[0]['geometry']['lng']
#         latitude  = result[0]["geometry"]["lat"]
# print(latitude,longitude)
def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(msg)
    # response = requests.get('127.0.0.1:8001/person/{}'.format(msg['from']['id']))
    # update['message']['chat']['first_name']
    # bot.sendMessage(-310500080,'привіт @newskit_bot ,як в тeбe справи?')
    if content_type =='sticker' and 'set_name'=='bundblyad':
        bot.sendMessage(chat_id,'*О ннііі,не бунтуйте будь-ласка*', parse_mode='Markdown')
    if content_type != 'text':
        bot.sendMessage(chat_id, "*Вибач,я розумію тільки текстові повідомлення😢*", parse_mode='Markdown')
        return
    command = msg['text']
    app_id = "f996f51b"
    app_key = "cdfb503fe8f18fe3784de8cdabf67581"

    if command =='Тижнева Погода':
        conn = sqlite3.connect('main_db.db')
        cur = conn.cursor()
        com_sql = "INSERT OR REPLACE INTO commands (user_id, location) VALUES (?, ?)"
        cur.execute(com_sql, (msg['from']['id'], '7'))
        conn.commit()
        bot.sendMessage(chat_id, 'Напиши своє місцезназодження')
    if command =='Погода на завтра':
        conn = sqlite3.connect('main_db.db')
        cur = conn.cursor()
        com_sql = "INSERT OR REPLACE INTO commands (user_id, location) VALUES (?, ?)"
        cur.execute(com_sql, (msg['from']['id'], '5'))
        conn.commit()
        bot.sendMessage(chat_id, 'Напиши своє місцезназодження')
    if command == '/start' :
        markup = ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text='Поточна Погода'),KeyboardButton(text='Погода на завтра'),KeyboardButton(text='Тижнева Погода')]
            ], resize_keyboard=True)
        bot.sendMessage(chat_id, '*Привіііт*', reply_markup=markup, parse_mode='Markdown')

    conn = sqlite3.connect('main_db.db')
    cur = conn.cursor()
    # cur.execute("SELECT EXISTS(SELECT * FROM commands WHERE user_id=msg['from']['id'])")
    print(msg['from']['id'])
    cur.execute("SELECT EXISTS(SELECT user_id,location FROM commands WHERE user_id={} and location='1')".format(msg['from']['id']))
    result = cur.fetchall()
    print(result)
    if result == [(1,)] and command!='/start' and command!='Поточна Погода' and command!='Тижнева Погода' and command!='Погода на завтра':
        print(command)
        #deletion of smth in table
        conn = sqlite3.connect('main_db.db')
        sql = 'DELETE FROM commands WHERE user_id=?'
        cur = conn.cursor()
        cur.execute(sql, (msg['from']['id'],))
        conn.commit()
        #end deletion

        try:
            # encoding location
            key = 'a279f5ab7cc1464da34cec0183dde7a0'
            geocoder = OpenCageGeocode(key)
            query=command
            result = geocoder.geocode(query)
            if result and len(result):
                longitude = result[0]['geometry']['lng']
                latitude  = result[0]["geometry"]["lat"]
            # end encoding location
                #getting weather
            r = requests.get('http://api.weatherunlocked.com/api/trigger/{},{}/current temperature gt 16 includecurrent?app_id=f996f51b&app_key=cdfb503fe8f18fe3784de8cdabf67581'.format(latitude,longitude))
            print (r.json())
            Weather = r.json()
            FinalWeather='*' +'Поточна погода у '+command +'*'+':'+'\n'+'🌡️ Температура: '+str(round(Weather['CurrentWeather']['temp_c']))+'°C'+'\n'+'🌡️ Відчувається як: '+str(round(Weather['CurrentWeather']['feelslike_c']))+'°C'+ '\n'+ '💦 Вологість: '+str(round(Weather['CurrentWeather']['humid_pct']))+'%'+'\n'+'💨 Вітер: '+str(round(Weather['CurrentWeather']['windspd_ms']))+'м/с'
            # bot.sendMessage(chat_id,FinalWeather,parse_mode='HTML')
            # bot.sendPhoto(chat_id,'https://techcrunch.com/wp-content/uploads/2017/05/onedrive-illo3.jpg?w=730&crop=1',caption=FinalWeather,parse_mode='MARKDOWN')
            icon= Weather['CurrentWeather']['wx_icon']
            final_icon= icon.replace('.gif', '.png') or icon.replace('.png', '.png')
            print(final_icon)
            bot.sendPhoto(chat_id,open('icons/{}'.format(final_icon), 'rb'),caption=FinalWeather,parse_mode='MARKDOWN')
            admin= msg['from']['first_name']+command+"Успішно запитав поточну погоду"
            bot.sendMessage(462005869,admin)
            print(FinalWeather)
            #end getting weather
        except UnboundLocalError or ConnectionError :
            bot.sendMessage(chat_id,'Ти неправильно написав(-ла) місцезназодження.Натисни на кнопку *Поточна Погода* щоб спробувати щераз',parse_mode='Markdown')

    if result ==[(0,)]:

        # bot.sendMessage(chat_id,"test no location")
     pass
    conn = sqlite3.connect('main_db.db')
    cur = conn.cursor()
    # cur.execute("SELECT EXISTS(SELECT * FROM commands WHERE user_id=msg['from']['id'])")
    print(msg['from']['id'])
    cur.execute("SELECT EXISTS(SELECT user_id,location FROM commands WHERE user_id={} and location='7')".format(msg['from']['id']))
    result2 = cur.fetchall()
    print('Week' +str(result2))
    if result2 == [(1,)] and command!='/start' and command!='Поточна Погода' and command!='Тижнева Погода' and command!='Погода на завтра':
        print(command)
        #deletion of smth in table
        conn = sqlite3.connect('main_db.db')
        sql = 'DELETE FROM commands WHERE user_id=?'
        cur = conn.cursor()
        cur.execute(sql, (msg['from']['id'],))
        conn.commit()
        #end deletion

        try:
            # encoding location
            key = 'a279f5ab7cc1464da34cec0183dde7a0'
            geocoder = OpenCageGeocode(key)
            query=command
            result = geocoder.geocode(query)
            if result and len(result):
                longitude = result[0]['geometry']['lng']
                latitude  = result[0]["geometry"]["lat"]
            # end encoding location
                #getting weather
            r = requests.get('http://api.weatherunlocked.com/api/trigger/{},{}/forecast tomorrow temperature gt 16 include7dayforecast?app_id=f996f51b&app_key=cdfb503fe8f18fe3784de8cdabf67581'.format(latitude,longitude))

            # r = requests.get('http://api.weatherunlocked.com/api/trigger/{},{}/current temperature gt 16 includecurrent?app_id=f996f51b&app_key=cdfb503fe8f18fe3784de8cdabf67581'.format(latitude,longitude))
            print (r.json())
            Weather = r.json()
            Days=Weather['ForecastWeather']['Days']
            Today='🔶 ' +'Сьогодні,'+'*'+ str(Days[0]['date'])+'*'+':'+'\n'+'      🌡️ Температура: '+str(round(Days[0]['temp_min_c']))+'°' +' - '+str(round(Days[0]['temp_max_c']))+'°C'+'\n'+'      💧 Ймов. опадів: '+str(round(Days[0]['prob_precip_pct']))+'%'+ '\n'+'      💦 Вологість: '+str(round(Days[0]['humid_min_pct']))+' - '+str(round(Days[0]['humid_max_pct']))+'%'+'\n'+'      💨 Вітер: '+str(round(Days[0]['windgst_max_ms']))+' м/с'
            Day2='\n'+'🔶 '+ 'Завтра,'+ '*'+str(Days[1]['date'])+'*'+':'+'\n'+'      🌡️ Температура: '+str(round(Days[1]['temp_min_c']))+'°' +' - '+str(round(Days[1]['temp_max_c']))+'°C'+'\n'+'      💧 Ймов. опадів: '+str(round(Days[1]['prob_precip_pct']))+'%'+ '\n'+'      💦 Вологість: '+str(round(Days[1]['humid_min_pct']))+' - '+str(round(Days[1]['humid_max_pct']))+'%'+'\n'+'      💨 Вітер: '+str(round(Days[1]['windgst_max_ms']))+' м/с'
            Day3='\n'+'🔶 '+ '*'+str(Days[2]['date'])+'*'+':'+'\n'+'      🌡️ Температура: '+str(round(Days[2]['temp_min_c']))+'°' +' - '+str(round(Days[2]['temp_max_c']))+'°C'+'\n'+'      💧 Ймов. опадів: '+str(round(Days[2]['prob_precip_pct']))+'%'+ '\n'+'      💦 Вологість: '+str(round(Days[2]['humid_min_pct']))+' - '+str(round(Days[2]['humid_max_pct']))+'%'+'\n'+'      💨 Вітер: '+str(round(Days[3]['windgst_max_ms']))+' м/с'
            Day4='\n'+'🔶 '+ '*'+str(Days[3]['date'])+'*'+':'+'\n'+'      🌡️ Температура: '+str(round(Days[3]['temp_min_c']))+'°' +' - '+str(round(Days[3]['temp_max_c']))+'°C'+'\n'+'      💧 Ймов. опадів: '+str(round(Days[3]['prob_precip_pct']))+'%'+ '\n'+'      💦 Вологість: '+str(round(Days[3]['humid_min_pct']))+' - '+str(round(Days[3]['humid_max_pct']))+'%'+'\n'+'      💨 Вітер: '+str(round(Days[3]['windgst_max_ms']))+' м/с'
            Day5='\n'+'🔶 '+ '*'+str(Days[4]['date'])+'*'+':'+'\n'+'      🌡️ Температура: '+str(round(Days[4]['temp_min_c']))+'°' +' - '+str(round(Days[4]['temp_max_c']))+'°C'+'\n'+'      💧 Ймов. опадів: '+str(round(Days[4]['prob_precip_pct']))+'%'+ '\n'+'      💦 Вологість: '+str(round(Days[4]['humid_min_pct']))+' - '+str(round(Days[4]['humid_max_pct']))+'%'+'\n'+'      💨 Вітер: '+str(round(Days[4]['windgst_max_ms']))+' м/с'
            Day6='\n'+'🔶 '+ '*'+str(Days[5]['date'])+'*'+':'+'\n'+'      🌡️ Температура: '+str(round(Days[5]['temp_min_c']))+'°' +' - '+str(round(Days[5]['temp_max_c']))+'°C'+'\n'+'      💧 Ймов. опадів: '+str(round(Days[5]['prob_precip_pct']))+'%'+ '\n'+'      💦 Вологість: '+str(round(Days[5]['humid_min_pct']))+' - '+str(round(Days[5]['humid_max_pct']))+'%'+'\n'+'      💨 Вітер: '+str(round(Days[5]['windgst_max_ms']))+' м/с'
            Day7='\n'+'🔶 '+ '*'+str(Days[6]['date'])+'*'+':'+'\n'+'      🌡️ Температура: '+str(round(Days[6]['temp_min_c']))+'°' +' - '+str(round(Days[6]['temp_max_c']))+'°C'+'\n'+'      💧 Ймов. опадів: '+str(round(Days[6]['prob_precip_pct']))+'%'+ '\n'+'      💦 Вологість: '+str(round(Days[6]['humid_min_pct']))+' - '+str(round(Days[6]['humid_max_pct']))+'%'+'\n'+'      💨 Вітер: '+str(round(Days[6]['windgst_max_ms']))+' м/с'
            print(Today)
            FinalWeather='*' +'Тижнева погода у '+command +'*'+'\n'+Today+Day2+Day3+Day4+Day5+Day6+Day7
            # bot.sendMessage(chat_id,FinalWeather,parse_mode='HTML')
            # bot.sendPhoto(chat_id,'https://techcrunch.com/wp-content/uploads/2017/05/onedrive-illo3.jpg?w=730&crop=1',caption=FinalWeather,parse_mode='MARKDOWN')
            print(FinalWeather)
            bot.sendMessage(chat_id,FinalWeather,parse_mode='MARKDOWN')
            admin= msg['from']['first_name']+"Успішно запитав тижневу погоду,місто - "+command
            bot.sendMessage(462005869,admin)
            print(FinalWeather)
            #end getting weather
        except UnboundLocalError or ConnectionError :
            bot.sendMessage(chat_id,'Ти неправильно написав(-ла) місцезназодження.Натисни на кнопку *Тижнева Погода* щоб спробувати щераз',parse_mode='Markdown')

    if command =='Поточна Погода':

        conn = sqlite3.connect('main_db.db')
        cur = conn.cursor()
        com_sql = "INSERT OR REPLACE INTO commands (user_id, location) VALUES (?, ?)"
        cur.execute(com_sql, (msg['from']['id'], '1'))
        conn.commit()
        bot.sendMessage(chat_id, 'Напиши своє місцезнаходження')

    conn = sqlite3.connect('main_db.db')
    cur = conn.cursor()
    # cur.execute("SELECT EXISTS(SELECT * FROM commands WHERE user_id=msg['from']['id'])")
    print(msg['from']['id'])
    cur.execute("SELECT EXISTS(SELECT user_id,location FROM commands WHERE user_id={} and location='5')".format(msg['from']['id']))
    result3 = cur.fetchall()
    print('Week' +str(result3))
    if result3 == [(1,)] and command!='/start' and command!='Поточна Погода' and command!='Тижнева Погода' and command!='Погода на завтра':
        #deletion of smth in table
        conn = sqlite3.connect('main_db.db')
        sql = 'DELETE FROM commands WHERE user_id=?'
        cur = conn.cursor()
        cur.execute(sql, (msg['from']['id'],))
        conn.commit()
        #end deletion

        try:
            # encoding location
            key = 'a279f5ab7cc1464da34cec0183dde7a0'
            geocoder = OpenCageGeocode(key)
            query=command
            result = geocoder.geocode(query)
            if result and len(result):
                longitude = result[0]['geometry']['lng']
                latitude  = result[0]["geometry"]["lat"]
            # end encoding location
                #getting weather
            r = requests.get('http://api.weatherunlocked.com/api/trigger/{},{}/forecast tomorrow temperature gt 16 include7dayforecast?app_id=f996f51b&app_key=cdfb503fe8f18fe3784de8cdabf67581'.format(latitude,longitude))

            # r = requests.get('http://api.weatherunlocked.com/api/trigger/{},{}/current temperature gt 16 includecurrent?app_id=f996f51b&app_key=cdfb503fe8f18fe3784de8cdabf67581'.format(latitude,longitude))
            print (r.json())
            Weather = r.json()
            Days=Weather['ForecastWeather']['Days']
            Day2='*'+str(Days[1]['date'])+'*'+':'+'\n'+'🌡️ Температура: '+str(round(Days[1]['temp_min_c']))+'°' +' - '+str(round(Days[1]['temp_max_c']))+'°C'+'\n'+'💧 Ймов. опадів: '+str(round(Days[1]['prob_precip_pct']))+'%'+ '\n'+'💦 Вологість: '+str(round(Days[1]['humid_min_pct']))+' - '+str(round(Days[1]['humid_max_pct']))+'%'+'\n'+'💨 Вітер: '+str(round(Days[1]['windgst_max_ms']))+' м/с'
            print(Day2)
            FinalWeather='*' +'Завтрашня погода у '+command +'*'+ '\n'+Day2

            bot.sendMessage(chat_id,FinalWeather,parse_mode='MARKDOWN')
            admin= msg['from']['first_name']+"Успішно запитав тижневу погоду,місто - "+command
            bot.sendMessage(462005869,admin)
            #end getting weather
        except UnboundLocalError or ConnectionError :
            bot.sendMessage(chat_id,'Ти неправильно написав(-ла) місцезназодження.Натисни на кнопку *Завтрашня Погода* щоб спробувати щераз',parse_mode='Markdown')
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
