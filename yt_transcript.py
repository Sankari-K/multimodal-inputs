import re
import subprocess
import os
import urllib.parse 

from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
from pydub import AudioSegment
from vosk import Model, KaldiRecognizer
import wave
import json

def is_valid_yt_link(link):
    return re.match(r"^(https?\:\/\/)?((www\.)?youtube\.com|youtu\.be)\/.+$", link)

def get_yt_video_id(link):
    if "shorts" in link:
        index = link.index("shorts")
        return link[index + len("shorts/"):]
    
    url_data = urllib.parse.urlparse(link)
    query = urllib.parse.parse_qs(url_data.query)
    return query["v"][0]

def process_transcript(transcript):
    return " ".join([sentence["text"].replace("\n", " ") for sentence in transcript])

def get_yt_transcript(link):
    if not is_valid_yt_link(link):
        raise Exception("Invalid link provided. Must provide valid youtube link.")
    
    video_id = get_yt_video_id(link) 
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=("en", "en-US"))
        return process_transcript(transcript)
    except Exception as e:
        print("Making transcript...")
        
        audio = YouTube(link).streams.get_audio_only()
        audio.download(filename="audiofile.mp4")
        
        # if .wav exists already, remove it
        if os.path.isfile("./audiofile.wav"):
            os.remove("audiofile.wav")

        command = "ffmpeg -i ./audiofile.mp4 -ab 160k -ac 2 -ar 44100 -vn ./audiofile.wav"
        subprocess.call(command, shell=True)
        os.remove("audiofile.mp4")

        audio = AudioSegment.from_wav("audiofile.wav") # load audio file
        audio = audio.set_channels(1) # convert to mono
        audio = audio.set_frame_rate(16000) # set frame rate
        audio.export("audiofile.wav", format="wav") # save new audio

        model = Model("./model")    # https://alphacephei.com/vosk/models
        recognizer = KaldiRecognizer(model, 16000)

        audio_file = wave.open("audiofile.wav", "rb")
        transcribed_text = []

        while True:
            data = audio_file.readframes(4000)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                transcribed_text.append(result['text'])
        
        final_result = json.loads(recognizer.FinalResult())
        transcribed_text.append(final_result['text'])

        os.remove("audiofile.wav")
        
        return ". ".join(transcribed_text)
