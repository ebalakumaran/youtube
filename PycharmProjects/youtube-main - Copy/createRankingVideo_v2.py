from moviepy.editor import *
import numpy as np
from moviepy.video.tools.segmenting import findObjects
from vectortween.PointAnimation import PointAnimation

#create a video using thumbnail
def create_thumbnail_video(duration,):
    # load video
    #clip = VideoFileClip(file_path)
    # getting duration of the video
    #duration = clip.duration
    #print("duration : ", duration)
    # creating slide for each image
    img_clips = []
    i=0
    while i < duration:
        slide = ImageClip("thumbnail.png", duration=2)
        img_clips.append(slide)
        i += 2


    # concatenating slides
    video_slides = concatenate_videoclips(img_clips, method='compose')
    # exporting final video
    video_slides.write_videofile("thumbnail_video.mp4", fps=24)

def create_blank_video(size, duration, fps=25, color=(0,0,0), output='blank_video.mp4'):
    ColorClip(size, color, duration=duration).write_videofile(output, fps=fps)

import moviepy.editor as mp
def create_blank_video_with_audio():
    audio = mp.AudioFileClip("tamil_open_1.mp3")
    video1 = mp.VideoFileClip("blank_video.mp4")
    final = video1.set_audio(audio)
    final.write_videofile("blank_video_with_audio.mp4", codec='mpeg4', audio_codec='libvorbis')

#create rank_1 video multple times to the length of audio duration
def create_rank_1_video(audio_duration):
    # load video
    clip = VideoFileClip("rank_1_video.mp4")
    # getting duration of the video
    rank_1_clip_duration = clip.duration
    print("rank_1_clip_duration : ", rank_1_clip_duration)
    # creating slide for each image
    rank_1_clips = []
    i =rank_1_clip_duration
    while i < audio_duration:
        videoFileClip = VideoFileClip("rank_2_video.mp4")
        rank_1_clips.append(videoFileClip)
        i += rank_1_clip_duration
    # concatenating videos
    print(rank_1_clips)
    final = concatenate_videoclips(rank_1_clips, method='compose')
    final.write_videofile("C:\\Users\\rkurian\\PycharmProjects\\pythonProject1\\videos\\trial\\rank_1_final_video.mp4", threads=16, codec='libx264', preset="slow", ffmpeg_params=['-b:v', '10000k'])


def create_winners_video(duration, text_clip, screen_size, viewCount):
    texts = []
    starts = []
    durations = []
    txt_clips = []
    i = 0


    #small_screen_video = VideoFileClip("C:\\Users\\rkurian\\PycharmProjects\\pythonProject1\\videos\\trial\\3.mp4", audio=True). \
    #    subclip(10 + 33, 60 + 50). \
    #    crop(486, 180, 1196, 570)
    ranking_video = VideoFileClip("blank_video_with_audio.mp4",
                                       audio=True)#. \
        #crop(486, 180, 1196, 570)
    w, h = moviesize = ranking_video.size
    print("main video w,h : " , w,h )

    #thumbnail video DOWNSIZED, HAS A WHITE MARGIN, IS IN THE TOP Center
    small_screen_video = (VideoFileClip("thumbnail_video.mp4", audio=False).
             #resize((w/3,h/3)).    # one third of the total screen
             resize(.75).
             margin( 6,color=(139,101,8)).  #white margin
             margin( bottom=20, right=20, opacity=0). # transparent
             set_pos(('right', 'center')))

    # process rank_1_final video
    rank1_video = (VideoFileClip("C:\\Users\\rkurian\\PycharmProjects\\pythonProject1\\videos\\trial\\rank_1_final_video.mp4", audio=False).
                          resize(0.99).  # one third of the total screen
                          #margin(6, color=(255, 255, 255)).  # white margin
                          margin(bottom=20, right=20, opacity=0).  # transparent
                          set_pos(('left','center')) )
                          #set_pos(lambda t: ('center', 50+t)))
                          #set_pos((w/2, h/2+100)))


    txt = TextClip(text_clip, font='Amiri-regular',
                       color='white',size=(400, 0),fontsize=24).set_duration(duration)

    txt_col = txt.on_color(size=(ranking_video.w + txt.w,txt.h-10),
                      color=(0,0,0), pos=(10,'center'), col_opacity=0.6)


    # THE TEXT CLIP IS ANIMATED.
    # I am *NOT* explaining the formula, understands who can/want.
    txt_mov = txt_col.set_pos( lambda t: (max(w/w,int(w-0.5*w*t)),
                                      max(5*h/6,int(100*t))) )
    # setting position of text

    add_text = TextClip(text_clip,font="SakalBharati", fontsize=50, method="pango", color="white").set_duration(duration)
    #add_text = add_text.set_pos('bottom').set_duration(duration)
    add_text = add_text.set_duration(duration).set_position(position)



    # add some celebration
    celebrationsImage = ImageClip("celebrations.png").set_start(0).set_duration(duration).set_pos(("center", "top")).set_opacity(.99)

    video_list = [ranking_video,celebrationsImage,rank1_video, small_screen_video,add_text, ]
    while i < duration:
        texts.append(viewCount)
        starts.append(i)
        durations.append(2)
        i += 3

    for text, t, text_duration in zip(texts, starts, durations):
        txt_clip = TextClip(text, fontsize=150, color='red', font="Keep-Calm-Medium", kerning=-2, interline=-1,
                            stroke_color="white", stroke_width=2)
        txt_clip = txt_clip.set_start(t).set_duration(text_duration)
        txt_clip = txt_clip.set_pos('center')
        # txt_clips.append(txt_clip)
        video_list.append(txt_clip)




    #celebrationsImageGif = VideoFileClip(("congratulations.gif"), has_mask=True, target_resolution=(400, 400)).set_pos((500,300))
    #celebrationsImageGif = VideoFileClip(("celebrations.gif"), has_mask=True, target_resolution=(400, 300)).set_pos(("center", "center"))
    #celebrationsImageGif.set_position(lambda t: ('center', 500 + (1080-500)*(t/5)))
    # FINAL ASSEMBLY
    #final = CompositeVideoClip([ranking_video,celebrationsImage,rank1_video,add_text, small_screen_video,celebrationsImageGif.set_start(5).crossfadein(1)])
    final = CompositeVideoClip(video_list)

    final.subclip(0,3).write_videofile("C:\\Users\\rkurian\\PycharmProjects\\pythonProject1\\videos\\trial\\1_winner_rank1.mp4",threads=16,fps=30,codec='libx264')


def position(t):
        df = duration * fps
        tf = t * fps
        return na_pt.make_frame(tf, 0, 0, df / 4, df, None)







if __name__ == "__main__":
    #load audio file
    audioclip = AudioFileClip("tamil_open_2.mp3")
    #find duration of audio file
    duration = audioclip.duration
    print("duration : ", duration)
    text_clip = "Winner is - குழந்தை பெயர்கள்"
    len_text_clip = len(text_clip)
    text_clip = text_clip.encode('utf8')
    #len_text_clip = len(text_clip)
    print(len_text_clip)
    viewCount = "60000 Views"
    size = (2024, 1024)
    W= 2024
    H = 1024
    #end_x_offset = W/2-W/3-len_text_clip
    #max char can accommodate is 60. Each char occupies 33pix/2 (for font size = 50). So to make it center , perform below calculations
    end_x_offset = W/2- (len_text_clip*16.5)
    print(end_x_offset)
    end_y_offset = H-H/10
    fps = 25
    na_pt = PointAnimation((end_x_offset, 0), (end_x_offset, end_y_offset), tween=['easeOutBounce'], ytween=['easeOutBounce'])

    #create_thumbnail_video(duration)
    #create_blank_video(size,duration)
    #create_blank_video_with_audio()
    #create_rank_1_video(duration)
    create_winners_video(duration, text_clip,size, viewCount)