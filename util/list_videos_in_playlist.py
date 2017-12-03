import credentials
import requests, sys

request = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={}&key={}".format(sys.argv[1], credentials.key)
resp = requests.get(request).json()
for item in resp['items']:
    for thing in item['snippet']:
        print thing
