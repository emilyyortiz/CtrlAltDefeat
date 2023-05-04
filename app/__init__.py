from flask import Flask, render_template, session, request, redirect
import sqlite3
import os #?
#more imports for other files later
from api_handle import *
from table_handle import *


app = Flask(__name__)

#for later
#app.secret_key - os.urandom(32)

#i forgot difference between get/post!
#code not shamelessly repurposed from p3
@app.route('/', methods=['GET'])
def login():
    if 'username' in session:
        return redirect('/home')
    return render_template('login.html') #names subject to change

@app.route('/register', methods=['GET'])
def register():
  return render_template('register.html')

@app.route('/signup', methods=['GET', 'POST'])
def make_account():
  if user_exist(request.form.get('username')):
    return render_template('register.html', status='Username is in use!')

  #new entry
  if (request.form.get('password') != request.form.get('password-confirm')):
    return render_template('register.html', status='The passwords typed are not the same!')
  create_user(request.form.get('username'), request.form.get('password'))
  session['username'] = request.form['username']
  return redirect('/home')
  
@app.route('/auth', methods=['GET', 'POST'])
def authenticate():
  if not verify(request.form.get('username'), request.form.get('password')):
    return render_template('login.html', status='Incorrect login info')
  session['username'] = request.form['username']
  return redirect('/home')

#TODO: 
#Way to add and save playlists
#Display wordcloud on playlist
#Rip lyrics for wordcloud AND display
#Select songs to play
#Play songs
#Search query entry from html, dubbed "entry" for the request
@app.route('/home', methods=['GET', 'POST'])
def home():
    #maybe unnecessary? 
    if !('username' in session):
        return redirect('/')
    return render_template('index.html')


if __name__ == '__main__':
    app.debug = True
    app.run()