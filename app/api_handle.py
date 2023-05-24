import requests
import json
import os
# from serpapi import GoogleSearch

# working with musixmatch and wordcloud APIs
# Functions meant to be called (more details above functions):
# music_api(text)

# THIS FUNCTION IS NOT MEANT TO BE CALLED BY FLASK OR OTHER OUTSIDE FILES
# takes in search phrase
# searches for the phrase in titles and artists
# returns array of top 3 results
# [
#   {
#     "id": 87181813,
#     "title": "On Top Of The World",
#     "artist": "Imagine Dragons"
#   },
#   {
#     "id": 88774856,
#     "title": "Top Of The World",
#     "artist": "Carpenters"
#   },
#   {
#     "id": 247221810,
#     "title": "Top Of The World",
#     "artist": "Shawn Mendes"
#   }
# ]
def music_search(text):
    url = "https://api.musixmatch.com/ws/1.1/track.search?"

    path = os.path.dirname(os.path.realpath(__file__)) # path to current python file
    
    key = open(path + "/keys/key_api0", "r").read()
    key = key.strip()
    # key = "test"

    querystring = {
        "apikey": key,
        "q_track_artist": text, # search for title and artist
        "s_track_rating": "desc", # most popular track first
        "page": 1, # one page
        "page_size": 3, # 3 results
    }

    response = requests.get(url, params=querystring).json()
    # print(json.dumps(response, indent=2))

    if(response["message"]["header"]["status_code"] == 200):
        # array where each element is a dictionary representing a song
        track_list = response["message"]["body"]["track_list"]
        # print(json.dumps(track_list, indent=2))
        
        output = []

        # pick specific data from each song dictionary
        for i in range(len(track_list)):
            song_data = track_list[i]["track"] # dict with all data for one song
            # print(json.dumps(song_data, indent=2))
            song_dict = {}
            song_dict["id"] = song_data["track_id"]
            song_dict["title"] = song_data["track_name"]
            song_dict["artist"] = song_data["artist_name"]
            output.append(song_dict)

        return output
    
    return 'error'

# music_search() test cases ==============================================================
# print("title")
# test = music_search("top of the world")
# print(json.dumps(test, indent=2))

# print("artist")
# test = music_search("shawn mendes")
# print(json.dumps(test, indent=2))

# print("title by artist")
# test = music_search("top of the world by shawn mendes")
# print(json.dumps(test, indent=2))

# print("title - artist")
# test = music_search("top of the world - shawn mendes")
# print(json.dumps(test, indent=2))


# takes in search phrase
# searches for the phrase in titles and artists
# returns array of top 3 results
# each array element is a dict containing the following
# {
#     "id": 247221810,
#     "title": "Top Of The World",
#     "artist": "Shawn Mendes",
#     "lyrics": "<insert lyrics here>"}
# }
def music_api(text):
    output = music_search(text) # array of dicts, each containing song id, title, artist
    if (output == 'error'):
        return 'error'

    url = "https://api.musixmatch.com/ws/1.1/track.lyrics.get?"

    path = os.path.dirname(os.path.realpath(__file__)) # path to current python file
    
    key = open(path + "/keys/key_api0", "r").read()
    key = key.strip()
    # key = "test"

    for i in range(len(output)):
        querystring = {
            "apikey": key,
            "track_id": output[i]["id"]
        }

        response = requests.get(url, params=querystring).json()
        # print(json.dumps(response, indent=2))

        if (response["message"]["header"]["status_code"] == 200):
            output[i]["lyrics"] = response["message"]["body"]["lyrics"]["lyrics_body"]
        else:
            return 'error'

    return output

# music_api() test cases
# test = music_api("top of the world - shawn mendes")
# test = music_api("hello")
# print(test)
# print(json.dumps(test, indent=2))

def wordcloud_api(text):
    url = "https://quickchart.io/wordcloud"   

    path = os.path.dirname(os.path.realpath(__file__)) # path to current python file
    
    key = open(path + "/keys/key_api0", "r").read()
    key = key.strip()

    querystring = {
        "text": text  
    }
    print(response = requests.get(url, params=querystring).json())

# wordcloud_api("to be or not to be that is the question")

# to do list
# we r supposed to show copyright lol
# check musixmatch checklist
# make sure i only get lyrics for songs with lyrics
# error message in case api call is bad
# post thing in case text input is too big

# https://quickchart.io/documentation/word-cloud-api/


# https://serpapi.com/search.json?engine=youtube&search_query=star+wars

# takes in text, returns url for top yt search result
# be careful, limit is 100 calls per month
# no error handling
def yt_api(text):
    url = "https://serpapi.com/search.json?engine=youtube"   

    path = os.path.dirname(os.path.realpath(__file__)) # path to current python file
    
    key = open(path + "/keys/key_api1", "r").read()
    key = key.strip()
    # key = "bcf1f8ef75efb2d2556095a49c736cc0f1806d13167b809e027e8a6c1b12b62c"

    querystring = {
        "api_key": key,
        "search_query": text  
    }

    results = requests.get(url, params=querystring).json()
    # print(json.dumps(results, indent=2))
    output_url = results["video_results"][0]["link"]
    return output_url

# print("hello-adele")
# print(yt_api("hello-adele"))
# print("sex sells - lovejoy")
# print(yt_api("sex sells - lovejoy"))


# {'error': 'Invalid API key. Your API key should be here: https://serpapi.com/manage-api-key'}
