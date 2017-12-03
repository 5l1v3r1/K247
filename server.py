from flask import Flask
from flask import request
from flask import render_template
import sqlite3 as sql
import time
import requests
import isodate
import random
import urlparse
import credentials

start_time = time.time()

app = Flask(__name__, template_folder = 'templates')

@app.route('/')
def player():
    global start_time
    video_time = (time.time() - start_time)
    playlist_data = list_videos()
    current_video = find_place(video_time, playlist_data)
    if (playlist_data):
        current_video, video_start, time_left = find_place(video_time, playlist_data)
        print video_start
        return render_template('player.html', current_video = current_video, video_time = video_time, video_start = video_start, time_left = time_left, video_list = playlist_data)
    else:
        start_time = time.time()
        return render_template('addvideo.html')

@app.route('/del', methods=['GET', 'POST'])
def delete_item():
    data = request.args['id']
    video_watched(data)
    return data

@app.route('/add', methods=['GET', 'POST'])
def parse_request():
    data = request.args['test']
    print data
    list = [x.strip() for x in data.split(',')]
    for item in list:
        if len(item) > 30:
            url_data = urlparse.urlparse(item)
            video = urlparse.parse_qs(url_data.query)["v"]
            item = video[0]
        add_video(item, '0', 'test')
    return data

@app.route('/clear')
def clear():
    clear_videos()
    return "cleared"

def find_place(video_time, video_list):
    #videos_played=[]
    for video in video_list:
        #videos_played.append(video[0])
        prev_time = int(video_time)
        video_time = int(int(video_time) - int(video[4]))
        if video_time < 0:
            return video[1], str(prev_time), str(int(video[4]-prev_time))
        else:
            video_watched(video[0])
    return "Out of videos"
    
def video_watched(video_id):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("delete from video where id = {}".format(video_id))
    print video_id
    con.commit()

def minutes_to_seconds(t):
    h, m, s = [int(i) for i in t.split(':')]
    return 3600*h + 60*m + s
    
def add_video(url, votes, comment):
    key = 'AIzaSyCvbQP7gvAltepnEkPUa9EMkZ_F6u9W_X0'
    video_details = get_video_data(url, key)
    video_title = get_video_title(url, key)
    video_duration = minutes_to_seconds(str(isodate.parse_duration(video_details['items'][0]['contentDetails']['duration'])))
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO video (url, votes, comment, duration) VALUES (?,?,?,?)", (url, votes, video_title, video_duration))
    con.commit()
    
    
    #con.close()
def get_video_data(url, key):
    request = "https://www.googleapis.com/youtube/v3/videos?id={}&part=contentDetails&key={}".format(url, key)
    r = requests.get(request)
    return r.json()

def get_video_title(url,key):
    request = "https://www.googleapis.com/youtube/v3/videos?id={}&part=snippet&key={}".format(url, key)
    r = requests.get(request)
    print r
    return r.json()['items'][0]['snippet']['title']

    
def list_videos(params=()):
    con = sql.connect("database.db")
    cur = con.cursor()
    if params==():
        result = cur.execute("select * from video")
    else:
        string = "select"
        for i in xrange(len(params)-1):
            string +="%s,"
        string +="%s"
        string += " from video"
        result = cur.execute(string)
   # con.close()
    print result
    return result.fetchall()

def clear_videos():
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("delete from video")
    con.commit()
                        
