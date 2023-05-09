from flask import Flask, render_template, session, request, redirect
import sqlite3
import os #?
#more imports for other files later
from api_handle import *
from table_handle import *


app = Flask(__name__)

#for later
app.secret_key = os.urandom(32)

#i forgot difference between get/post!
#code not shamelessly repurposed from p3
@app.route('/', methods=['GET'])
def login():
    if 'username' in session: #when cookie work
    #if(False):
        return redirect('/home')
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
  if (request.form.get('password') != request.form.get('password-confirm')):
    return render_template('register.html', status='The passwords typed are not the same!')
  create_user(request.form.get('username'), request.form.get('password')) #NEED method to create an entry in the table
  session['username'] = request.form['username']
  print(session['username'])
  return redirect('/') #/home or /
  
@app.route('/auth', methods=['GET', 'POST'])
def authenticate():
  if not check_pass(request.form.get('username'), request.form.get('password')): #NEED method to take in a username and password and return if that entry exists
  #if(False):
    return render_template('login.html', status='Incorrect login info')
  session['username'] = request.form['username']
  return redirect('/home')

#TODO: 
#Display wordcloud on playlist  OUTLINED
#Rip lyrics for wordcloud AND display  OUTLINED
#Select songs to play  OUTLINED
#Play songs from button  OUTLINED
#Search query entry from html, "entry" for the request

#MAIN ISSUES: 
#should the cover be updated every time the page is viewed? Seems intensive on the API
@app.route('/home', methods=['GET', 'POST'])
def home():
    #maybe unnecessary? 
    if ('username' in session):
        return redirect('/')
    return render_template('index.html')

'''
#returns a dictionary with the number of instances of each word in a playlist: 
pl = [] #String array of songs in playlist
dic = {string w : int num} #future dictoinary containing all words in playlist

#SAVE INFORMATION AS JSON OR ARRAY?
link = []  #string array of links to be used to play audio (if this becomes the used method)
artist = []  #string array of artist names to be displayed
current_song =  #necessary? pass in argument from form-action in HTML

#get playlist method, load into array, find song information
for(song : playlist):

  lyric = get_lyrics(song)
  #get lyric method

  #ALSO GET MORE INFORMATION ABOUT THE SONG TO DISPLAY! (FROM API)
  #artist name
  #song name
  #song link
  link[].append(get_link(song))

  #parsing of a dictionary for wordcloud
  for word in lyric.split(): #splits by spaces hopefully
    if(lyric.get(word)==none):
      lyric[word].append(1)
    else:
      lyric[word].update({word: lyric.get(word) + 1})
      
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

if __name__ == '__main__':
    app.debug = True
    app.run()