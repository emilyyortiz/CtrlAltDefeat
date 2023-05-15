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
  session.pop('username')
  return redirect('/')

@app.route('/search', methods=['GET', 'POST'])
def query():
  query = request.form.get('songInput')
  print(query)
  if query == None:
    query = "pl"
  return redirect('/home/' + query)

#TODO: 
#Display wordcloud on playlist  OUTLINED
#Rip lyrics for wordcloud AND display  OUTLINED
#Select songs to play  OUTLINED
#Play songs from button  OUTLINED
#Search query entry from html, "entry" for the request

#BIG ISSUE: 
#Where do we put a song into the playlist? 

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


    #if song is default playlist, wordcloud update is necessary
    if(que == "pl"):
      print("\n\nplaylist stuff: ")
      #gets the playlist for this user
      pl = user_playlist(session['username'])
      print(pl)
      print(len(pl))

      '''
      #collective lyrics
      lyrics = ""

      #INFORMATION IS ALL SAVED WITHIN THE PLAYLIST ARRAY OF DICTIONARIES
      #link = []  #string array of links to be used to play audio (if this becomes the used method)
      #artist = []  #string array of artist names to be displayed
      current_song = pl[0] #necessary? pass in argument from form-action in HTML

      #get playlist method, load into array, find song information
      
      for(song in pl[0]):

        lyric = get_lyrics(song.get("name"))
        #get lyric method

        #ALSO GET MORE INFORMATION ABOUT THE SONG TO DISPLAY! (FROM API)
        #artist name
        #song name
        #song link
        #link[].append(song.get("link")) #when links come into play

        #parsing of a dictionary for wordcloud
        for word in lyric.split(): #splits by spaces hopefully
          if(dic.get(word)==none):
            dic[word].append(1)
          else:
            dic[word].update({word: lyric.get(word) + 1})
            
      #wordcloud method
      cloud = get_cloud(lyric)

      return render_template('index.html', 
      word_cloud = cloud, 
      YTlinks = link, 
      playlist = pl, 
      artists = artist, 
      cur = current_song)

      #PAGE TAKES: 
      # A image (?) type word cloud
      # An array of youtube links
      # An array of song names
      # An array of artist names
      # The current song being played
    '''
    #if viewing a song not in playlist
    else:
      print("\n\n DEBUG: \n Query: ")
      print(que)
      search_res = music_api(que)
      current_song = search_res[0]
      print("cursong: ")
      print(current_song)
      #print("full search: " + music_api(query))
      #reference: 
      # {
      # "id": 247221810,
      # "title": "Top Of The World",
      # "artist": "Shawn Mendes",
      # "lyrics": "<insert lyrics here>"}
      # }

      #test_cloud = wordcloud_api(current_song.get('lyrics'))
      #print("\n\ncloud: " )
      #print(test_cloud)




  return render_template('index.html')


if __name__ == '__main__':
    app.debug = True
    app.run()