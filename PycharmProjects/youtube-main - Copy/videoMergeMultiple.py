from moviepy.editor import *
import os
import glob
import math

transition_video ='C:\\Users\\User\\PycharmProjects\\youtube-main\\complete video creation\\transition.mp4'

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
        print("Clip Size of ", video, end=" : ")
        print(value)
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
            print( "resizing the video... ")
            final = cur_clip.fx(vfx.resize, width=target_width, height = target_height)
            # save final clip
            resized_video_name = "resized_"+ video.replace(".\\", '')
            #video_list.remove(video)
            video_list_to_merge.append(resized_video_name)
            final.write_videofile(resized_video_name)
        else:
            video_list_to_merge.append(video)
        #print("Pref Width x Pref Height of clip 2 : ", end=" ")
        #print(str(target_width) + " x ", str(target_height))

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
        print("Clip Size of ", video, end=" : ")
        print(value)
        #cur_clip = resize_and_center(cur_clip)
        clips.append(cur_clip)
        clips.append(transition_clip)
    # concatenating all the elements of clips array
    final = concatenate_videoclips(clips,method='compose')
    #final = concatenate_videoclips(clips, method="chain") # use this with resize_and_center(cur_clip)
    final.write_videofile("merged.mp4",threads=16,codec='libx264',preset="slow",ffmpeg_params=['-b:v','10000k'])
    #final.write_videofile("merged.mp4", fps=20,threads=16,codec='libx264',preset="slow",ffmpeg_params=['-b:v','10000k'])



if __name__ == "__main__":
    merge_video("C:\\Users\\User\\PycharmProjects\\youtube-main\\complete video creation\\mergingFolder")
