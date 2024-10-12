# -*- coding: utf-8 -*-
"""add_transcipt.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1aiSs2zC2ib_1-V0lCIHknMznUm8PM8W1
"""

!pip install moviepy==2.0.0.dev2
!pip install imageio==2.25.1

from google.colab import drive
drive.mount('/content/drive')

!pip install openai

mp4filename = "/content/drive/My Drive/python_file/input_video.mp4"
from openai import OpenAI
api_key = "your api key"
client = OpenAI(api_key=api_key)
with open(mp4filename, "rb") as audio_file:
    # Call Whisper's audio transcription API and request srt format
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="srt"
    )
with open("subtitles1.srt", "w") as srt_file:
    srt_file.write(transcription)



!apt install imagemagick

!cat /etc/ImageMagick-6/policy.xml | sed 's/none/read,write/g'> /etc/ImageMagick-6/policy.xml

!pip install pysrt==1.1.2

import sys
import pysrt
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

srtfilename = "/content/drive/My Drive/python_file/subtitles1.srt"
def time_to_seconds(time_obj):
    return time_obj.hours * 3600 + time_obj.minutes * 60 + time_obj.seconds + time_obj.milliseconds / 1000


def create_subtitle_clips(subtitles, videosize,fontsize=24, font='Arial', color='red', debug = False):
    subtitle_clips = []

    for subtitle in subtitles:
        start_time = time_to_seconds(subtitle.start)
        end_time = time_to_seconds(subtitle.end)
        duration = end_time - start_time

        video_width, video_height = videosize

        text_clip = TextClip(subtitle.text, fontsize=fontsize, font=font,bg_color = 'black',color=color,size=(video_width*3/4, None), method='caption').set_start(start_time).set_duration(duration)
        subtitle_x_position = 'center'
        subtitle_y_position = video_height* 4 / 5

        text_position = (subtitle_x_position, subtitle_y_position)
        subtitle_clips.append(text_clip.set_position(text_position))

    return subtitle_clips

video = VideoFileClip(mp4filename)
subtitles = pysrt.open(srtfilename)

begin,end= mp4filename.split(".mp4")
output_video_file = begin+'_subtitled'+".mp4"

print ("Output file name: ",output_video_file)

# Create subtitle clips
subtitle_clips = create_subtitle_clips(subtitles,video.size)

# Add subtitles to the video
final_video = CompositeVideoClip([video] + subtitle_clips)

# Write output video file
final_video.write_videofile(output_video_file)