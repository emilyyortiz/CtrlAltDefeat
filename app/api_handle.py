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
    # make sure i only get lyrics for songs with lyrics

# music_api("Blank Space")

# takes in 
# [{title:
#   artist:
#   lyrics:}]
def music_search(text):
    url = "https://api.musixmatch.com/ws/1.1/track.search?"

    path = os.path.dirname(os.path.realpath(__file__)) # path to current python file
    
    key = open(path + "/keys/key_api0", "r").read()
    key = key.strip()

    querystring = {
        "apikey": key,
        "q_track_artist": text, # search for title and artist
        "s_track_rating": "desc", # most popular track first
        "page": 1, # one page
        "page_size": 3, # 3 results
    }

    response = requests.get(url, params=querystring).json()
    # print(json.dumps(response, indent=2))

    # array where each element is a dictionary representing a song
    track_list = response["message"]["body"]["track_list"]
    # print(json.dumps(track_list, indent=2))
    
    output = []

    for i in range(len(track_list):
        song_data = track_list[i]["track"] # dict with all data for one song
        print(json.dumps(song_data, indent=2))
        song_dict["title"] = song_data["track_name"]
        song_dict["artist"] = song_data["artist_name"]
        output.append(song_dict)

    return output
    response = requests.get(url, params=querystring).json()
    print(response)

print(music_search("Blue Danube"))

# we r supposed to show copyright lol
# check musixmatch checklist