import json, urlparse, isodate, requests, time
import sqlite3 as sql


class otv_robot(object):
    def __init__(self, key):
        print "initted"
        self.key = key
        self.con = sql.connect("database.db")
        self.cur = self.con.cursor()
        
    def find_place(self,video_time, video_list):
        for video in video_list:
            prev_time = int(video_time)
            video_time = int(int(video_time) - int(video[4]))
            if video_time < 0:
                return video[1], str(prev_time), str(int(video[4]-prev_time))
            else:
                video_watched(video[0])
            return video_list[0][0], "0", "0"

    def read_videos(self,video_file):
        self.clear_db()
        with open(video_file) as data_file:    
            video_l = json.load(data_file)
        for video in video_l["videos"]:
            self.add_video(video)
        
    def minutes_to_seconds(self,t):
        h, m, s = [int(i) for i in t.split(':')]
        return 3600*h + 60*m + s
    
    def add_video(self,url):
        # Handle long urls or video ids]
        if len(url) > 30:
            url_data = urlparse.urlparse(url)
            url = urlparse.parse_qs(url_data.query)["v"][0]
        
        video_details = self.get_video_data(url, self.key, "contentDetails")
        video_snippet = self.get_video_data(url, self.key, "snippet")
        video_title = video_snippet['items'][0]['snippet']['title']
        video_duration = self.minutes_to_seconds(str(isodate.parse_duration(video_details['items'][0]['contentDetails']['duration'])))
        con = sql.connect("database.db")
        cur = con.cursor()
        cur.execute("INSERT INTO video (url, votes, comment, duration) VALUES (?,?,?,?)", (url, "0", video_title, video_duration))
        con.commit()
    
    def get_video_data(self,url, key, part): #contentDetails or snippet
        request = "https://www.googleapis.com/youtube/v3/videos?id={}&part={}&key={}".format(url,part, key)
        r = requests.get(request)
        return r.json()
    
    def list_videos(self,params=()):
        result = self.cur.execute("select * from video")
        return result.fetchall()

    def clear_db(self):
        self.cur.execute("delete from video")
        self.con.commit()
    

                        
