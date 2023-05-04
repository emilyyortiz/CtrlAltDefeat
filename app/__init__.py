from flask import Flask, render_template, session, request, redirect
import sqlite3
import os #?
#more imports for other files later

app = Flask(__name__)

#for later
#app.secret_key - os.urandom(32)

#Landing page, only page? 
#i forgot difference between get/post!
@app.route('/', methods=['GET', 'POST'])
def placeholder():
    return render_template('foo.html')


if __name__ == '__main__':
    app.debug = True
    app.run()