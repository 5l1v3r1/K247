from flask import Flask
from flask import request
from flask import render_template
import sqlite3 as sql
import time
import requests
import isodate
import json
import urlparse
import credentials
import k247

start_time = time.time()
otv_player = k247.otv_robot(credentials.key)
app = Flask(__name__, template_folder = 'templates')

otv_player.read_videos("data/videos.json")

@app.route('/')
def player():
    global start_time
    video_time = (time.time() - start_time)
    playlist_data = otv_player.list_videos()
    if (playlist_data):
        current_video, video_start, time_left = otv_player.find_place(video_time, playlist_data)
        print video_start
        return render_template('player.html', current_video = current_video, video_time = video_time, video_start = video_start, time_left = time_left, video_list = playlist_data)
    else:
        start_time = time.time()
        return "oops we out"
