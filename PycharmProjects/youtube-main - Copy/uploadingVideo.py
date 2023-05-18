import re
import moviepy.editor as mp
from moviepy.editor import *
from gtts import gTTS

import pandas as pd

data = pd.read_csv('data_open_tamil.csv', index_col=0)
data = data.apply(pd.to_numeric, errors='coerce')
last_row = data.iloc[-1]
top_columns = last_row.nlargest(3).index.tolist()

def create_thumbnail_video(duration,filename):
    # load video
    #clip = VideoFileClip(file_path)
    # getting duration of the video
    #duration = clip.duration
    #print("duration : ", duration)
    # creating slide for each image
    img_clips = []
    i=0
    while i < duration:
        #2 - Saregama TV Shows Tamil ( INIYA Serial).png
        #3 - Sun TV ( Vanathai Pola).png
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


    txt = TextClip(text_clip, font='C:\\Users\\User\\AppData\\Local\\Microsoft\\Windows\\Fonts\\Latha.ttf',color='white',size=(400, 0),fontsize=20).set_duration(duration)
    txt_col = txt.on_color(size=(ranking_video.w + txt.w,txt.h-10),
                      color=(0,0,0), pos=(10,'center'), col_opacity=0.6)

    txt_mov = txt_col.set_pos( lambda t: (max(w/w,int(w-0.5*w*t)),
                                      max(5*h/6,int(100*t))) )

    add_text = TextClip(text_clip, fontsize=30, color="white").set_duration(duration)
    add_text = add_text.set_pos('bottom').set_duration(duration)

    #add some celebration
    celebrationsImage = ImageClip("celebrations.png").set_start(0).set_duration(duration).set_pos(("center", "top")).set_opacity(.99)
    video_list = [ranking_video, celebrationsImage, rank1_video, add_text, small_screen_video, ]
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

for i in range(2,3):
    print(i)
    text = ''
    name = re.findall(r'^(.+)\.png$', selected_files[i])[0]
    with open(f"C:\\Users\\User\\PycharmProjects\\youtube-main\\video_desc_tamil\\{name}.txt", "r", encoding='utf-8') as f:
        text = f.read()
    language = 'ta'
    tts = gTTS(text=text, lang=language)
    tts.save("tamil_open_"+str(i+1)+".mp3")
for i in range(2,3):
    #load audio file
    audioclip = AudioFileClip(audiofiles[i])
    #find duration of audio file
    duration = audioclip.duration
    text_clip=''
    if i==0:
        text_clip = "Winner - "+videos_full_names[i]+"\n\n\n"
    if i==1:
        text_clip = "2nd Place - "+videos_full_names[i]+"\n\n\n"
    if i==2:
        text_clip = "3rd Place - "+videos_full_names[i]+"\n\n\n"
    size = (2024, 1024)
    views = convert_number(int(videos_views_count[i]))
    print(videos_views_count[i])
    print(views)
    print(text_clip)
    create_thumbnail_video(duration,selected_files[i])
    create_blank_video(size,duration)
    create_blank_video_with_audio(audiofiles[i])
    create_rank_video(duration,i+1)
    create_winners_video(duration, text_clip,size,final_file_names[i],i+1,str(views)+" Views")
