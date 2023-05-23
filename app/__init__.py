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
  #print(check_pass(request.form.get('username'), request.form.get('password')))
  #print("login " + request.form.get('username') + " " + request.form.get('password'))
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
  query = query.replace(")", ") ")
  query = query.replace(".", " ")
  query = query.replace("/", " ")
  if query == None or query.strip() == "" or "\\" in query.strip():
    query = "pl"
  
  return redirect('/home/' + query.strip())

@app.route('/add', methods=['GET','POST'])
def add():
  user = session["username"]
  title = request.args.get("title")
  artist = request.args.get("artist")
  lyrics = request.args.get("lyrics")
  add_playlist(user, title, artist, lyrics)
  return redirect("/home/" + title + " - " + artist)


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


    print("\n\nplaylist stuff: ")
    #gets the playlist for this user
    pl = user_playlist(session['username'])
    #print(pl)

    collective = []

    #INFORMATION IS ALL SAVED WITHIN THE PLAYLIST TUPLE OF ARRAYS
    #get playlist method, load into array, find song information
    for num in range(len(pl[0])):

      #Explaining structure for future reference: 
        #The title of the song is the i-th element in the first array of the playlist tuple
        #The current song element is the first element of the returned search
      search_res = music_api(pl[0][num])
      if len(search_res) > 0 and search_res != "error":
        current_song = search_res[0]
        #print(current_song)
        #get lyric method
        if(que == "pl"):
          lyrics += current_song.get('lyrics')
        #lyrics test  
        #print("COMBINED LYRICS: " + lyrics)
        
        #ALSO GET MORE INFORMATION ABOUT THE SONG TO DISPLAY! (FROM API)
        #artist name
        #song name
        #song link
        #link[].append(song.get("link")) #when links come into play
        cur_log = [current_song.get("title"), current_song.get("artist")]
        collective.append(cur_log)
    #print(collective)
      


    #if viewing a song not in playlist
    if(que != "pl"):
      print("\n\n DEBUG: \n Query: ")
      print(que)
      search_res = music_api(que)
      #print(search_res)
      if len(search_res) > 0 and search_res != "error":
        current_song = search_res[0]
        #print("cursong: ")
        #print(current_song)
        lyrics = current_song.get('lyrics')
      else: 
        current_song = "error"
        
      
      #print("full search: " + music_api(query))
      #reference: 
      # {
      # "id": 247221810,
      # "title": "Top Of The World",
      # "artist": "Shawn Mendes",
      # "lyrics": "<insert lyrics here>"}
      # }


  #cleanse lyrics
  lyrics = lyrics.replace("******* This Lyrics is NOT for Commercial use *******", " ")
  lyrics = lyrics.replace("\n", " ")
  lyrics = lyrics.replace(")", ") ")
  lyrics = lyrics.replace(".", " ")
  lyrics = lyrics.replace("/", " ")[:-15]
  #print("COMBINED LYRICS " + lyrics)

  #WORD CLOUD TEST
  cloud = "https://quickchart.io/wordcloud?removeStopwords=true&text=" + lyrics
  #print(cloud)

  #error case on search due to song not existing or api dying
  if current_song == "error": 
    cur_song = "Enter another song! We don't have this one"
    return render_template('index.html',
    song = cur_song
    #playlist = collective
    )

  #if there are songs in the playlist, mainly used for default and searches
  if current_song is not None: 
    cur_song = current_song.get('title')
    cur_artist = current_song.get('artist')
    cur_lyrics = current_song.get('lyrics')

    #A special cleanse of lyrics for use in webpage
    cur_lyrics = cur_lyrics.replace("******* This Lyrics is NOT for Commercial use *******", "")[:-15]
    print(cur_lyrics)

    return render_template('index.html',
    song = cur_song, 
    artist = cur_artist,
    lyrics = cur_lyrics,
    word_cloud = cloud
    #playlist = collective
    )
  
  #specific case of not having anything in the playlist
  else: 
    return render_template('index.html')


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