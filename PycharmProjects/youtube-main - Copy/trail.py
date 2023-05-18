import requests
from datetime import datetime, timedelta
import pymysql
import moviepy.editor as mp
import bar_chart_race as bcr
import pandas as pd
from moviepy.editor import *
import glob
import math
from gtts import gTTS
import openai
from googletrans import Translator
from pathlib import Path

translator = Translator(service_urls=['translate.googleapis.com'])


translator = Translator(service_urls=['translate.googleapis.com'])

db = pymysql.connect(host='database-1.clbwnv9wuuzw.us-east-1.rds.amazonaws.com',
                                 user='admin',
                                 password='bu$$iN3$$', charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
cursor = db.cursor()
sql = 'use tamil'
cursor.execute(sql)

openai.api_key = "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"

start_sequence = "\nAI:"
restart_sequence = "\nHuman: "

prompt = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman: "

def openai_create(prompt):

    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    temperature=0.9,
    max_tokens=150,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0.6,
    stop=[" Human:", " AI:"]
    )

    return response.choices[0].text



import re

import unicodedata

def is_tamil(word):
    for c in word:
        if unicodedata.name(c).startswith('TAMIL'):
            continue
        elif c.isalpha():
            return False
    return True


def remove_special_chars_and_emojis(word):
    return re.sub(r'[\/\\\:\*\?\"\<\>\|\(\)]', '', word)

def remove_emoji(text):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

def otherlang_eng(text):
    translator = Translator()
    english_word = translator.translate(text, src='ta', dest='en').text
    return english_word


filename = "video_names_file.txt"
with open(filename, "w") as file:
    file.write("")

filename_1 = "video_views_file.txt"
with open(filename_1, "w") as file:
    file.write("")

import os
folder_path = ["video_desc_tamil","video_thumbnails_tamil","video_channel_logo"]
for folder in folder_path:
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Error deleting {filename}: {e}")


# folder_path = "C:\\Users\\User\\PycharmProjects\\youtube-main\\mergingFolder"
# allowed_names = ["1.mp4","2.mp4","7.mp4"]
#
# for file_path in glob.glob(folder_path + "/*.mp4"):
#     file_name = os.path.basename(file_path)
#     if file_name not in allowed_names:
#         os.remove(file_path)


topicID={'Music':'/m/04rlf','Gaming':'/m/0bzvm2','Sports':'/m/06ntj','Entertainment':'/m/02jjt','Lifestyle':'/m/019_rr','Society':'/m/098wr','Knowledge':'/m/01k8wb'}
#topicList=['Music','Gaming','Sports','Entertainment','Lifestyle','Society','Knowledge']
topicList=['Music']
APIkeys=[]
#languages=['tamil','malayalam']
languages=['tamil']
languagescode={'tamil':'ta','malayalam':'ml'}

today = datetime.today().date()
yesterday = today - timedelta(days=1)
day_before_yesterday = today - timedelta(days=2)
yesterday_str = yesterday.strftime('%Y-%m-%d')
day_before_yesterday_str = day_before_yesterday.strftime('%Y-%m-%d')

import os
import glob

files = glob.glob('bar_image_labels/*')
for f in files:
    os.remove(f)

sql = f"Select time_video,date_video FROM Data_24hrs_open WHERE (date_video = '"+str(day_before_yesterday_str)+"' AND time_video >= '12:29:00') or (date_video = '"+str(today)+"' AND time_video <= '12:31:00') or (date_video='"+str(yesterday_str)+"');"
cursor.execute(sql)
time_date_index = cursor.fetchall()
timelist=[]
datelist=[]
prev=''
for times in time_date_index:
    if times['time_video'] != prev:
        timelist.append(times['time_video'])
        datelist.append(times['date_video'])
        prev=times['time_video']
timelist_demo=timelist
from datetime import datetime, timedelta

nearest_hour_list = []
for time_value in timelist_demo:
    dt = datetime.strptime(time_value, '%H:%M:%S')
    rounded_dt = (dt.replace(second=0, microsecond=0, minute=0)
                  + timedelta(hours=dt.minute // 30))
    nearest_hour_value = rounded_dt.strftime('%H:%M:%S')
    nearest_hour_list.append(nearest_hour_value)

timelist_demo=nearest_hour_list
datelist_demo=datelist
timelist_demo.append('12:30:00')
timelist_demo.append('12:30:00')
timelist_demo.append('12:30:00')
timelist_demo.append('12:30:00')
datelist_demo.append(datetime.today().strftime('%Y-%m-%d'))
datelist_demo.append(datetime.today().strftime('%Y-%m-%d'))
datelist_demo.append(datetime.today().strftime('%Y-%m-%d'))
datelist_demo.append(datetime.today().strftime('%Y-%m-%d'))
timelist_demo.append('12:30:00')
timelist_demo.append('12:30:00')
timelist_demo.append('12:30:00')
timelist_demo.append('12:30:00')
datelist_demo.append(datetime.today().strftime('%Y-%m-%d'))
datelist_demo.append(datetime.today().strftime('%Y-%m-%d'))
datelist_demo.append(datetime.today().strftime('%Y-%m-%d'))
datelist_demo.append(datetime.today().strftime('%Y-%m-%d'))

merged_list = []

for i in range(len(timelist_demo)):
    merged_value = f"{datelist[i]} {timelist_demo[i]}"
    merged_list.append(merged_value)

sql = f"Select * FROM Data_24hrs_open WHERE (published_date = '"+str(day_before_yesterday_str)+"' AND published_time >= '12:29:00') or (published_date = '"+str(yesterday_str)+"' AND published_time <= '12:31:00');"
cursor.execute(sql)
data_window = cursor.fetchall()

obj={}
obj['time']=merged_list

for lang in languages:
    print("Top videos in open category : ")

    url = "https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=10&type=video&publishedAfter="+day_before_yesterday_str+"T12:29:00Z&publishedBefore="+str(today)+"T12:31:00Z&q="+lang+"&relevanceLanguage="+languagescode[f"{lang}"]+"&key=AIzaSyDIuol_UZWN88c5q0R9oIJ3pyy2XfeLPy0&order=viewCount"
    print(url)
    res = requests.get(url)
    if res.status_code == 200:
        response=res.json()
        val=1
        print("Language : " + lang+" | Total Results : "+str(response['pageInfo']['totalResults']))
        for r in response['items']:
            if val<=10:

                urlStats = "https://www.googleapis.com/youtube/v3/videos?part=statistics&id="+r['id']['videoId']+"&key=AIzaSyDIuol_UZWN88c5q0R9oIJ3pyy2XfeLPy0"
                resStats = requests.get(urlStats)
                if resStats.status_code == 200:
                    stats = resStats.json()
                    emoji_removed = remove_emoji(r['snippet']['title'])
                    emoji_removed = emoji_removed.strip()
                    first_word = emoji_removed.split(" ")[0]
                    second_word = emoji_removed.split(" ")[1]
                    channelName = remove_emoji(r['snippet']['channelTitle'])
                    channelName = channelName.replace('|', '')

                    if is_tamil(first_word):
                        print("Tamil word : "+first_word)
                        first_word = otherlang_eng(first_word)
                        print("English word : "+first_word)
                    if is_tamil(second_word):
                        print("Tamil word : "+second_word)
                        second_word = otherlang_eng(second_word)
                        print("English word : "+second_word)
                    if is_tamil(channelName):
                        print("Tamil word : "+channelName)
                        channelName = otherlang_eng(channelName)
                        print("English word : "+channelName)

                    if second_word=="-" or second_word=="|":
                        second_word=""

                    for stat in stats['items']:

                        likeCheck = 0
                        viewCheck = 0
                        commentCheck = 0

                        video_date = r['snippet']['publishedAt'][0:10]
                        video_time = r['snippet']['publishedAt'][11:-1]

                        for l in stat['statistics'].keys():
                            if str(l) == "likeCount":
                                likeCheck = stat['statistics']['likeCount']
                            if str(l) == "viewCount":
                                viewCheck = stat['statistics']['viewCount']
                            if str(l) == "commentCount":
                                commentCheck = stat['statistics']['commentCount']

                        urlLogo = "https://www.googleapis.com/youtube/v3/videos?part=snippet&id=" + r['id'][
                            'videoId'] + "&key=AIzaSyDIuol_UZWN88c5q0R9oIJ3pyy2XfeLPy0"
                        resLogo = requests.get(urlLogo)
                        if resLogo.status_code == 200:
                            Logo = resLogo.json()

                            # name = str(val) + "_" + r['snippet']['title'] + "_" + r['id']['videoId']
                            # name=remove_special_chars_and_emojis(r['snippet']['title'])
                            name = f"{str(val)} - {channelName} ( {first_word} {second_word})"
                            with open('video_names_file.txt','a',encoding="utf-8") as f_vnf:
                                f_vnf.write(name+" - "+r['snippet']['title']+"\n")
                            with open('video_views_file.txt', 'a', encoding="utf-8") as f_vnv:
                                f_vnv.write(name + " - " + stat['statistics']['viewCount'] + "\n")
                            for l in Logo['items']:
                                link_of_logo = l['snippet']['thumbnails']['high']['url']
                            response_logo = requests.get(link_of_logo)

                            with open("video_thumbnails_tamil/" + name+ ".png", "wb") as f:
                                f.write(response_logo.content)

                            output = openai_create(
                                f"Give a summary of the youtube video named as \" {r['snippet']['title']} \"")
                            translator = Translator(service_urls=['translate.googleapis.com'])
                            out = translator.translate(
                                output,
                                dest='ta'
                            )

                            with open("video_desc_tamil/" + name+ ".txt", "w",encoding="utf-8") as f:
                                f.write(out.text)

                        filtered_dicts = [d for d in data_window if d.get(
                            "video_id") == r['id']['videoId'] ]

                        views_count = []

                        index = 0
                        length = len(timelist)-1
                        while index < length:
                            flag = 0
                            for datas in filtered_dicts:
                                if datas['time_video'] == timelist[index] and datas['date_video'] == datelist[
                                    index]:
                                    views_count.append(datas['views'])
                                    flag = 1
                            if flag == 0 and (len(views_count) > 1) and (views_count[len(views_count) - 1] != 0):
                                views_count.append(views_count[len(views_count) - 1])
                            elif flag == 0:
                                views_count.append(0)
                            index += 1

                        views_count.append(stat['statistics']['viewCount'])
                        views_count.append(stat['statistics']['viewCount'])
                        views_count.append(stat['statistics']['viewCount'])
                        views_count.append(stat['statistics']['viewCount'])
                        views_count.append(stat['statistics']['viewCount'])
                        views_count.append(stat['statistics']['viewCount'])
                        views_count.append(stat['statistics']['viewCount'])
                        views_count.append(stat['statistics']['viewCount'])
                        views_count.append(stat['statistics']['viewCount'])

                        r['snippet']['title']=remove_special_chars_and_emojis(r['snippet']['title'])
                        # name = str(val) + "_" + r['snippet']['title'] + "_" + r['id']['videoId']

                        name = f"{str(val)} - {channelName} ( {first_word} {second_word})"

                        obj[name]=views_count

                        channelId = r['snippet']['channelId']
                        rlLogo = "https://www.googleapis.com/youtube/v3/channels?part=snippet&id=" + channelId + "&key=AIzaSyDIuol_UZWN88c5q0R9oIJ3pyy2XfeLPy0"
                        ch_resLogo = requests.get(rlLogo)
                        if ch_resLogo.status_code == 200:
                            ch_Logo = ch_resLogo.json()
                            # name = str(val) + "_" + r['snippet']['title'] + "_" + r['id']['videoId']
                            # name = remove_special_chars_and_emojis(name)

                            name = f"{str(val)} - {channelName} ( {first_word} {second_word})"
                            print(name)
                            for l in ch_Logo['items']:
                                link_of_logo = l['snippet']['thumbnails']['high']['url']
                            ch_response_logo = requests.get(link_of_logo)
                            with open("video_channel_logo/" + name + ".png", "wb") as f:
                                f.write(ch_response_logo.content)

                        print(str(val) + " - " + r['snippet']['title'] + " - " + r['snippet'][
                            'channelTitle'] + " - " +
                              video_date + " - " + video_time + " - " + stat['statistics']['viewCount'] + " - " +
                              stat['statistics']['likeCount'] + " - " + stat['statistics']['commentCount'])
                val+=1
            else:
                break
# data = pd.DataFrame(obj)
# data.to_csv('data_open_tamil.csv', index=False,encoding='utf-8')

data = pd.DataFrame.from_dict(obj)

data.to_csv('data_open_tamil.csv', index=False, encoding='utf-8-sig')


df=pd.read_csv('data_open_tamil.csv')
df=df.set_index('time')
bcr.bar_chart_race(df=df,
                   title="Top 10 videos across all category",
                   filename="C:\\Users\\User\\PycharmProjects\\youtube-main\\mergingFolder\\3.mp4",
                   img_label_folder="video_channel_logo"
                   # steps_per_period=10000,
                   # period_length=100,
                   # tick_image_mode='trailing',
                   # orientation='h',
                   # bar_size=.99,
                   # bar_textposition='outside',
                   # bar_texttemplate='{x:,.0f}',
                   # bar_label_font=5
                   )