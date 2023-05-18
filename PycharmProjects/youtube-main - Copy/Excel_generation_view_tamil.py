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
import re

import unicodedata

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
    if text=='' or text==None:
        return text
    translator = Translator()
    english_word = translator.translate(text, src='ta', dest='en').text
    return english_word


def remove_point_values(string):

    matches = re.findall(r'\d+\.\d+', string)
    for match in matches:
        rounded_value = str(round(float(match)))
        string = string.replace(match, rounded_value)

    return string


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


folder_path = "C:\\Users\\User\\PycharmProjects\\youtube-main\\mergingFolder"
allowed_names = ["1.mp4","2.mp4","7.mp4"]

for file_path in glob.glob(folder_path + "/*.mp4"):
    file_name = os.path.basename(file_path)
    if file_name not in allowed_names:
        os.remove(file_path)


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

dateList_changed=[]
for datevalue in datelist:
    date_obj=datetime.strptime(datevalue,'%Y-%m-%d')
    formatted_date=date_obj.strftime('%dth %b %Y')
    dateList_changed.append(formatted_date)
print(dateList_changed)
timelist_demo=nearest_hour_list
datelist_demo=dateList_changed
today=datetime.today()
formatted_date=today.strftime("%dth %b %Y")
timelist_demo.append('12:30:00')
timelist_demo.append('12:30:00')
timelist_demo.append('12:30:00')
timelist_demo.append('12:30:00')
datelist_demo.append(formatted_date)
datelist_demo.append(formatted_date)
datelist_demo.append(formatted_date)
datelist_demo.append(formatted_date)

timelist_demo.append('12:30:00')
timelist_demo.append('12:30:00')
timelist_demo.append('12:30:00')
timelist_demo.append('12:30:00')
datelist_demo.append(formatted_date)
datelist_demo.append(formatted_date)
datelist_demo.append(formatted_date)
datelist_demo.append(formatted_date)

merged_list = []

for i in range(len(timelist_demo)):
    merged_value = f"{datelist_demo[i]} {timelist_demo[i]}"
    merged_list.append(merged_value)

sql = f"Select * FROM Data_24hrs_open WHERE (published_date = '"+str(day_before_yesterday_str)+"' AND published_time >= '12:29:00') or (published_date = '"+str(yesterday_str)+"' AND published_time <= '12:31:00');"
cursor.execute(sql)
data_window = cursor.fetchall()

obj={}
obj['time']=merged_list

for lang in languages:
    print("Top videos in open category : ")
    today = datetime.today().date()
    url = "https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=10&type=video&publishedAfter="+day_before_yesterday_str+"T12:29:00Z&publishedBefore="+str(today)+"T12:31:00Z&q="+lang+"&relevanceLanguage="+languagescode[f"{lang}"]+"&key=AIzaSyDIuol_UZWN88c5q0R9oIJ3pyy2XfeLPy0&order=viewCount"
    print(url)
    res = requests.get(url)
    print(res.status_code)
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
                    first_word=remove_point_values(first_word)
                    second_word=remove_point_values(second_word)
                    channelName=remove_point_values(channelName)

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
                   filename="C:\\Users\\User\\PycharmProjects\\youtube-main\\mergingFolder\\barchart.mp4",
                   img_label_folder="C:\\Users\\User\\PycharmProjects\\youtube-main\\video_channel_logo"
                   # steps_per_period=10000,
                   # period_length=100,
                   # tick_image_mode='trailing',
                   # orientation='h',
                   # bar_size=.99,
                   # bar_textposition='outside',
                   # bar_texttemplate='{x:,.0f}',
                   # bar_label_font=5
                   )

# audio = mp.AudioFileClip("C:\\Users\\User\\PycharmProjects\\youtube-main\\barchart_audio.mp3")
# video1 = mp.VideoFileClip("C:\\Users\\User\\PycharmProjects\\youtube-main\\mergingFolder\\barchart.mp4")
# final = video1.set_audio(audio)
# final.write_videofile("C:\\Users\\User\\PycharmProjects\\youtube-main\\mergingFolder\\3.mp4",codec= 'mpeg4' ,audio_codec='libvorbis')
#
# file_path = Path("C:\\Users\\User\\PycharmProjects\\youtube-main\\mergingFolder\\barchart.mp4")
#
# if file_path.is_file():
#     file_path.unlink()
#     print("File deleted successfully.")
# else:
#     print("The file does not exist.")
#
import moviepy.editor as mp

def create_barchart_video_with_audio():
    audio = mp.AudioFileClip("C:\\Users\\User\\PycharmProjects\\youtube-main\\barchart_audio.mp3")
    video1 = mp.VideoFileClip("C:\\Users\\User\\PycharmProjects\\youtube-main\\mergingFolder\\barchart.mp4")
    duration = video1.duration
    final = video1.set_audio(audio).set_duration(duration)
    final.write_videofile("C:\\Users\\User\\PycharmProjects\\youtube-main\\mergingFolder\\3.mp4", codec='libx264', audio_codec='libmp3lame')

create_barchart_video_with_audio()
file_path = Path("C:\\Users\\User\\PycharmProjects\\youtube-main\\mergingFolder\\barchart.mp4")

if file_path.is_file():
    file_path.unlink()
    print("File deleted successfully.")
else:
    print("The file does not exist.")


import pandas as pd

data = pd.read_csv('data_open_tamil.csv', index_col=0)
data = data.apply(pd.to_numeric, errors='coerce')
last_row = data.iloc[-1]
top_columns = last_row.nlargest(3).index.tolist()

from vectortween.PointAnimation import PointAnimation

#create a video using thumbnail
def create_thumbnail_video(duration,filename):
    img_clips = []
    i=0
    while i < duration:
        slide = ImageClip("C:\\Users\\User\\PycharmProjects\youtube-main\\video_thumbnails_tamil\\"+filename, duration=2)
        img_clips.append(slide)
        i += 2

    # concatenating slides
    video_slides = concatenate_videoclips(img_clips, method='compose')
    # exporting final video
    video_slides.write_videofile("thumbnail_video.mp4", fps=24)

def create_blank_video(size, duration, fps=25, color=(0,0,0), output='blank_video.mp4'):
    ColorClip(size, color, duration=duration).write_videofile(output, fps=fps)

def create_blank_video_with_audio(filename):
    audio = mp.AudioFileClip(filename)
    video1 = mp.VideoFileClip("blank_video.mp4")
    final = video1.set_audio(audio)
    final.write_videofile("blank_video_with_audio.mp4", codec='mpeg4', audio_codec='libvorbis')

#create rank_1 video multple times to the length of audio duration
def create_rank_video(audio_duration,number):
    # load video
    clip = VideoFileClip("rank_"+str(number)+"_video.mp4")
    # getting duration of the video
    rank_1_clip_duration = clip.duration
    # creating slide for each image
    rank_1_clips = []
    i =rank_1_clip_duration
    while i < audio_duration:
        videoFileClip = VideoFileClip("rank_"+str(number)+"_video.mp4")
        rank_1_clips.append(videoFileClip)
        i += rank_1_clip_duration
    final = concatenate_videoclips(rank_1_clips, method='compose')
    final.write_videofile("rank_"+str(number)+"_final_video.mp4", threads=16, codec='libx264', preset="slow", ffmpeg_params=['-b:v', '10000k'])


def create_winners_video(duration, text_clip, screen_size,filename,number,viewCount):
    #small_screen_video = VideoFileClip("C:\\Users\\rkurian\\PycharmProjects\\pythonProject1\\videos\\trial\\3.mp4", audio=True). \
    #    subclip(10 + 33, 60 + 50). \
    #    crop(486, 180, 1196, 570)
    texts = []
    starts = []
    durations = []
    txt_clips = []
    i = 0
    ranking_video = VideoFileClip("blank_video_with_audio.mp4",
                                       audio=True)#. \
        #crop(486, 180, 1196, 570)
    w, h = moviesize = ranking_video.size

    #thumbnail video DOWNSIZED, HAS A WHITE MARGIN, IS IN THE TOP Center
    small_screen_video = (VideoFileClip("thumbnail_video.mp4", audio=False).
             resize((w/2,h/2)).    # one third of the total screen
             #resize(.99).
             margin( 6,color=(139,101,8)).  #white margin
             margin( bottom=20, right=20, opacity=0). # transparent
             set_pos(('right', 'center')))

    # process rank_1_final video
    rank1_video = (VideoFileClip("rank_"+str(number)+"_final_video.mp4", audio=False).
                          resize(0.99).  # one third of the total screen
                          #margin(6, color=(255, 255, 255)).  # white margin
                          margin(bottom=20, right=20, opacity=0).  # transparent
                          set_pos(('left','center')) )
                          #set_pos(lambda t: ('center', 50+t)))
                          #set_pos((w/2, h/2+100)))


    txt = TextClip(text_clip, font='Amiri-regular',color='white',size=(400, 0),fontsize=20).set_duration(duration)
    txt_col = txt.on_color(size=(ranking_video.w + txt.w,txt.h-10),
                      color=(0,0,0), pos=(10,'center'), col_opacity=0.6)

    txt_mov = txt_col.set_pos( lambda t: (max(w/w,int(w-0.5*w*t)),
                                      max(5*h/6,int(100*t))) )

    add_text = TextClip(text_clip,font="SakalBharati", fontsize=30, color="white",method="pango").set_duration(duration)
    #add_text = add_text.set_pos('bottom').set_duration(duration)
    add_text = add_text.set_duration(duration).set_position(position)

    #add some celebration
    celebrationsImage = ImageClip("celebrations.png").set_start(0).set_duration(duration).set_pos(("center", "top")).set_opacity(.99)
    video_list = [ranking_video, celebrationsImage, rank1_video, small_screen_video,add_text, ]
    while i < duration:
        texts.append(viewCount)
        starts.append(i)
        durations.append(2)
        i += 3

    for text, t, text_duration in zip(texts, starts, durations):
        txt_clip = TextClip(text, fontsize=130, color='red', font="Keep-Calm-Medium", kerning=-2, interline=-1,
                            stroke_color="white", stroke_width=2)
        txt_clip = txt_clip.set_start(t).set_duration(text_duration)
        txt_clip = txt_clip.set_pos('center')
        # txt_clips.append(txt_clip)
        video_list.append(txt_clip)

    #celebrationsImageGif = VideoFileClip(("congratulations.gif"), has_mask=True, target_resolution=(400, 400)).set_pos((500,300))
    # FINAL ASSEMBLY
    #final = CompositeVideoClip([ranking_video,celebrationsImage,rank1_video,add_text, small_screen_video])
    final = CompositeVideoClip(video_list)
    final.subclip(0,duration).write_videofile("C:\\Users\\User\\PycharmProjects\\youtube-main\\mergingFolder\\"+str(number+3)+".mp4",threads=16,fps=30,codec='libx264')

def convert_number(number):
    if number >= 10**12:
        return str(number // 10**11 / 10.0) + ' T+'
    elif number >= 10**9:
        return str(number // 10**8 / 10.0) + ' +'
    elif number >= 10**6:
        return str(number // 10**5 / 10.0) + ' M+'
    elif number >= 10**3:
        return str(number // 10**2 / 10.0) + ' K+'
    else:
        return str(number)


def contains_tamil_word(text):
    tamil_pattern = re.compile(r'[\u0B80-\u0BFF]+')  # Pattern to match Tamil characters

    # Search for Tamil characters in the text
    match = tamil_pattern.search(text)

    if match:
        return True  # Tamil characters found
    else:
        return False  # No Tamil characters found

def position(t):
    df = duration * fps
    tf = t * fps
    return na_pt.make_frame(tf, 0, 0, df / 4, df, None)


numbers = [str(column.split(' - ')[0]+" ") for column in top_columns]

audiofiles=['tamil_open_1.mp3','tamil_open_2.mp3','tamil_open_3.mp3']
final_file_names=['winner_1.mp4','winner_2.mp4','winner_3.mp4']
directory = "C:\\Users\\User\\PycharmProjects\\youtube-main\\video_thumbnails_tamil"
files = os.listdir(directory)
index=0
selected_files=[]
for index in range(0,3):
    for filename in files:
        if filename.startswith(numbers[index]):
            print(filename)
            selected_files.append(filename)
print(selected_files)
videos_full_names=[]
videos_views_count=[]
for filename in selected_files:
    name = re.findall(r'^(.+)\.png$', filename)[0]
    with open('C:\\Users\\User\\PycharmProjects\\youtube-main\\video_names_file.txt', 'r',
              encoding='utf-8') as file:
        text = file.read()
    line = next((l for l in text.split('\n') if name in l), None)
    if line:
        value = line.split(name)[1].strip(' - ')
        videos_full_names.append(value)

    with open('C:\\Users\\User\\PycharmProjects\\youtube-main\\video_views_file.txt', 'r',
              encoding='utf-8') as file:
        text = file.read()
    line = next((l for l in text.split('\n') if name in l), None)
    if line:
        value = line.split(name)[1].strip(' - ')
        videos_views_count.append(value)

print(videos_views_count)

for i in range(0,3):
    text = ''
    name = re.findall(r'^(.+)\.png$', selected_files[i])[0]
    with open(f"C:\\Users\\User\\PycharmProjects\\youtube-main\\video_desc_tamil\\{name}.txt", "r", encoding='utf-8') as f:
        text = f.read()
    language = 'ta'
    tts = gTTS(text=text, lang=language)
    tts.save("tamil_open_"+str(i+1)+".mp3")
for i in range(0,3):
    #load audio file
    audioclip = AudioFileClip(audiofiles[i])
    #find duration of audio file
    duration = audioclip.duration
    #duration=5
    text_clip=''
    video_name = str(videos_full_names[i])
    formattedString = ""
    if contains_tamil_word(video_name):
        for k in range(0, len(video_name), 65):
            formattedString += video_name[k:k + 65] + '\n'
    else:
        for k in range(0, len(video_name), 75):
            formattedString += video_name[k:k + 75] + '\n'
    if i==0:
        text_clip = "1st Place - "+formattedString+"\n\n\n"
    if i==1:
        text_clip = "2nd Place - "+formattedString+"\n\n\n"
    if i==2:
        text_clip = "3rd Place - "+formattedString+"\n\n\n"
    len_text_clip = len(text_clip)
    print(len_text_clip)
    text_clip=text_clip.encode('utf8')
    size = (2024, 1024)
    W= 2024
    H = 1024
    print(formattedString)
    print(formattedString.count('\n'))
    views = convert_number(int(videos_views_count[i]))
    end_x_offset=1024
    num_characters=0
    if (formattedString.count('\n')) > 1:
        first_newline_index = formattedString.find('\n')  # Find the index of the first newline character
        if first_newline_index != -1:  # If a newline character is found
            num_characters = first_newline_index
        else:  # If no newline character is found
            num_characters = len(text)
        print(num_characters)
        end_x_offset = W / 2 - (((num_characters) * 20) / 2)
    else:
        end_x_offset=W/2-((len(formattedString)*20)/2)
    print(end_x_offset)
    end_y_offset = H - H / 10
    print(end_y_offset)
    fps = 25
    na_pt = PointAnimation((end_x_offset, 0), (end_x_offset, end_y_offset), tween=['easeOutBounce'],
                           ytween=['easeOutBounce'])
    create_thumbnail_video(duration,selected_files[i])
    create_blank_video(size,duration)
    create_blank_video_with_audio(audiofiles[i])
    create_rank_video(duration,i+1)
    create_winners_video(duration, text_clip,size,final_file_names[i],i+1,str(views)+" Views")


transition_video ='C:\\Users\\User\\PycharmProjects\\youtube-main\\transition.mp4'

def resize_and_center(clip):
    clip_aspect_ratio = clip.w / clip.h

    target_aspect_ratio = target_width / target_height

    if clip_aspect_ratio >= target_aspect_ratio:
        scale_factor = target_height / clip.h
    else:
        scale_factor = target_width / clip.w

    clip = clip.resize(scale_factor)

    bg = ColorClip((target_width, target_height), color=(255, 255, 255))

    x = math.floor((target_width - clip.w) / 2)
    y = math.floor((target_height - clip.h) / 2)
    result = CompositeVideoClip([bg, clip.set_pos((x, y))])
    return result

# merge_video() takes directory path
def merge_video(directory):
    target_width = 0
    target_height = 0
    os.chdir(directory)
    video_list = glob.glob('./*.mp4')
    transition_clip = VideoFileClip(transition_video)

    #check the resolution of the video and convert in to same res for all videos
    for video in video_list:
        cur_clip = VideoFileClip(video)
        # getting clip size
        # getting width and height of clips
        w1 = cur_clip.w
        h1 = cur_clip.h
        value = cur_clip.size
        #print("Width x Height of clip 2 : ", end=" ")
        #print(str(w1) + " x ", str(h1))
        if target_width < w1:
            target_width = w1
        if target_height < h1:
            target_height = h1

    video_list_to_merge = []
    # applying resize filter
    for video in video_list:
        cur_clip = VideoFileClip(video)
        w1 = cur_clip.w
        h1 = cur_clip.h
        if target_width > w1 or target_height > h1 :
            final = cur_clip.fx(vfx.resize, width=target_width, height = target_height)
            # save final clip
            resized_video_name = "resized_"+ video.replace(".\\", '')
            #video_list.remove(video)
            video_list_to_merge.append(resized_video_name)
            final.write_videofile(resized_video_name)
        else:
            video_list_to_merge.append(video)

    # video_list contains list of all video file(mp4) in the folder
    clips = []
    # then we iterate over list to load video using VideoFileClip
    # and append it to clips list
    #os.chdir(directory)
    #video_list = glob.glob('./res*.mp4')
    for video in video_list_to_merge:
        cur_clip = VideoFileClip(video)
        # getting clip size
        value = cur_clip.size
        #cur_clip = resize_and_center(cur_clip)
        clips.append(cur_clip)
        clips.append(transition_clip)
    # concatenating all the elements of clips array
    final = concatenate_videoclips(clips,method='compose')
    #final = concatenate_videoclips(clips, method="chain") # use this with resize_and_center(cur_clip)
    final.write_videofile("merged.mp4",threads=16,codec='libx264',preset="slow",ffmpeg_params=['-b:v','10000k'])
    #final.write_videofile("merged.mp4", fps=20,threads=16,codec='libx264',preset="slow",ffmpeg_params=['-b:v','10000k'])


merge_video("C:\\Users\\User\\PycharmProjects\\youtube-main\\mergingFolder")
