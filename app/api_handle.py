import requests
import json
import os

#musixmatch + some sound api +_wordcloud

def music_api(text):
    url = "https://api.musixmatch.com/ws/1.1/track.lyrics.get?"
    # track.search?"
    
    path = os.path.dirname(os.path.realpath(__file__)) # path to current python file
    # print(path)
    key = open(path + "/keys/key_api0", "r").read()
    key = key.strip()
    # print(key)
    
    querystring = {
        "apikey": key,
        # "q_track": search
        "commontrack_id": 56420303
    }
# 56420303

    response = requests.get(url, params=querystring).json()
    print(response)

music_api("Blank Space")

# takes in 
# [{title:
#   artist:
#   lyrics:}]
def music_search(text):
    url = "https://api.musixmatch.com/ws/1.1/track.lyrics.get?"

    path = os.path.dirname(os.path.realpath(__file__)) # path to current python file
    
    key = open(path + "/keys/key_api0", "r").read()
    key = key.strip()

    querystring = {
            "apikey": key,
            "commontrack_id": 56420303
        }
    # 56420303

    response = requests.get(url, params=querystring).json()
    print(response)

    music_api("Blank Space")

# we r supposed to show copyright lol
# check musixmatch checklist