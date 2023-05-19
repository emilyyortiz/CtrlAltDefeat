from flask import Flask, render_template, session, request, redirect
import sqlite3
import os #?
#more imports for other files later
from api_handle import *
from table_handle import *


app = Flask(__name__)
app.app_context().push()

#for later
app.secret_key = os.urandom(32)



#i forgot difference between get/post!
#code not shamelessly repurposed from p3
@app.route('/', methods=['GET'])
def login():
    if 'username' in session: #when cookie work
    #if(False):
        return redirect('/home/pl')
    return render_template('login.html') #names subject to change

@app.route('/register', methods=['GET', 'POST'])
def register():
  return render_template('register.html')

@app.route('/signup', methods=['GET', 'POST'])
def make_account():
  if check_user(request.form.get('username')): #NEED a method to verify if a username is taken
  #if(False):
    return render_template('register.html', status='Username is in use!')

  #new entry
  print(request.form.get('password'))
  print(request.form.get('password_confirm'))
  if (request.form.get('password') != request.form.get('password_confirm')):
    return render_template('register.html', status='The passwords typed are not the same!')
  print("register " + request.form.get('username') + " " + request.form.get('password'))
  create_user(request.form.get('username'), request.form.get('password')) #NEED method to create an entry in the table
  session['username'] = request.form['username']
  print(session['username'])
  return redirect('/home/pl') #/home or /
  
#this method actually verifies whether or not the login works
@app.route('/auth', methods=['GET', 'POST'])
def authenticate():
  print(check_pass(request.form.get('username'), request.form.get('password')))
  print("login " + request.form.get('username') + " " + request.form.get('password'))
  if not (check_pass(request.form.get('username'), request.form.get('password'))): #NEED method to take in a username and password and return if that entry exists
  #if(False):
    return render_template('login.html', status='Incorrect login info')
  session['username'] = request.form['username']
  return redirect('/home/pl')

#forgot to actually allow a logout (I think it was in the site map)
@app.route('/logout')
def logout():
  #session.pop('username')
  print("popped user: " + 
  session.pop('username'))
  return redirect('/')

@app.route('/search', methods=['GET', 'POST'])
def query():
  query = request.form.get('songInput')
  print(query)
  if query == None:
    query = "pl"
  return redirect('/home/' + query)

#TODO: 
#Display wordcloud on playlist  DONE
#Rip lyrics for wordcloud AND display  DONE
#Select songs to play  OUTLINED
#Play songs from button  OUTLINED
#Search query entry from html, "entry" for the request DONE

#BIG ISSUE: 
#Where do we put a song into the playlist? RESOLVED
#How do we actually select a song? 

#MAIN ISSUES: 
#should the cover be updated every time the page is viewed? Seems intensive on the API
@app.route('/home/<que>', methods=['GET', 'POST'])
def home(que):

  #queri = request.args.get('que')
  #maybe unnecessary? 
  if ('username' not in session):
    return redirect('/')
  

  else: 
    current_song = None
    search_res = None
    #collective lyrics
    lyrics = ""


    #if song is default playlist, wordcloud update is necessary
    if(que == "pl"):

      #playlist population test
      #add_playlist(session['username'], "test", "tester", "testtesttest")


      print("\n\nplaylist stuff: ")
      #gets the playlist for this user
      pl = user_playlist(session['username'])
      print(pl)
      #print(len(pl))

      #INFORMATION IS ALL SAVED WITHIN THE PLAYLIST TUPLE OF ARRAYS

      #get playlist method, load into array, find song information
      
      for num in range(len(pl[0])):

        #Explaining structure for future reference: 
          #The title of the song is the i-th element in the first array of the playlist tuple
          #The current song element is the first element of the returned search
        current_song = music_api(pl[0][num])[0]
        print(current_song)
        #get lyric method
        lyrics += current_song.get('lyrics')
        #lyrics test  
        #print("COMBINED LYRICS: " + lyrics)
        
        #ALSO GET MORE INFORMATION ABOUT THE SONG TO DISPLAY! (FROM API)
        #artist name
        #song name
        #song link
        #link[].append(song.get("link")) #when links come into play

    #if viewing a song not in playlist
    else:
      print("\n\n DEBUG: \n Query: ")
      print(que)
      search_res = music_api(que)
      current_song = search_res[0]
      print("cursong: ")
      print(current_song)
      lyrics = current_song.get('lyrics')
      
      #print("full search: " + music_api(query))
      #reference: 
      # {
      # "id": 247221810,
      # "title": "Top Of The World",
      # "artist": "Shawn Mendes",
      # "lyrics": "<insert lyrics here>"}
      # }



      #test adds all searched songs to playlist 
      #add_playlist(session['username'], current_song['title'], current_song['artist'], current_song['lyrics'])

      #test_cloud = wordcloud_api(current_song.get('lyrics'))
      #print("\n\ncloud: " )
      #print(test_cloud)

  #cleanse lyrics
  lyrics = lyrics.replace("******* This Lyrics is NOT for Commercial use *******", " ")
  lyrics = lyrics.replace("...", " ")
  lyrics = lyrics.replace("\n", " ")
  lyrics = lyrics.replace(")", ") ")
  print("COMBINED LYRICS " + lyrics)

  #WORD CLOUD TEST
  cloud = "https://quickchart.io/wordcloud?removeStopwordss=true&text=" + lyrics

  cur_song = current_song.get('title')
  cur_artist = current_song.get('artist')
  cur_lyrics = current_song.get('lyrics')

  return render_template('index.html',
  song = cur_song, 
  artist = cur_artist,
  lyrics = cur_lyrics,
  word_cloud = cloud
  )
  


  '''
  return render_template('index.html', 
  word_cloud = cloud, 
  YTlinks = link, 
  playlist = pl, 
  artists = artist, 
  cur = current_song)
  '''

  #PAGE TAKES: 
  # A image (?) type word cloud
  # An array of youtube links
  # An array of song names
  # An array of artist names
  # The current song being played
    


if __name__ == '__main__':
    app.debug = True
    app.run()