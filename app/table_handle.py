import sqlite3
#rename maybe for playlist pizzaz

DB_FILE = "database.db"

db = None
db = sqlite3.connect(DB_FILE, check_same_thread = False)
c = db.cursor()

db.executescript("""
CREATE TABLE if not exists users(username text, password text);
Insert into users values(?,?), ('admin', 'password');
CREATE TABLE if not exists playlist(username text, song text, artist text, lyrics text);
""")

def db_connect():
    global db
    db = sqlite3.connect(DB_FILE)
    return db.cursor()

#---------------------------------------------------------------------------#
#LOGIN METHODS

#Creates a new user.
#Parameters: (text username, text password)
#Returns nothing
def create_user(username, password):
    try:
        c=db_connect()
        c.execute("Insert into users values(?,?)", (username, password))
        c.close()
        db.commit()
        db.close()
        print('User has been successfully created')
    except:
        print('User has not been created successfully')

#Checks if a username exists in the user table
#Parameters: (text username)
#Returns True if user exists, False if user does not exist
def check_user(username):
    c=db_connect()
    c.execute("Select username from users where username = ?", (username,))
    try:
        c.fetchone()[0]==username
        c.close()
        db.close()
        return True
    except: #If c.fetchone does not have an entry, then we want to catch the error and return an exception
        c.close()
        db.close()
        return False

#Checks if a password given matches the password of the username given 
#Parameters: (text username, text password)
#Returns True is password works, False if password does not match
def check_pass(username, password):
    c=db_connect()
    c.execute('select * from users where (username = ? AND password = ?)', (str(username), str(password)))
    try:
        c.fetchone()[0]
        c.close()
        db.close()
        return True
    except:
        c.close()
        db.close()
        return False

#----------------------------------------------------------------------------#
#PLAYLIST METHODS


#Adds username, song name, artist, lyrics to playlist nad assigns it an id
#Parameters: (text uername, text song, text artist, text lyrics)
#Returns nothing
def add_playlist(username, song, artist, lyrics):
    if(check_user(username) == False):
        print('Song has not been successfully added. Username does not exist in user database')
    else:
        try:
            c=db_connect()
            c.execute("Insert into playlist values(?,?,?,?)", (username, song, artist, lyrics))
            c.close()
            db.commit()
            db.close()
            print('Song has successfully been added')
        except:
            print('Song has not been successfully added')

#Removes row in playlist column with username and song name
#Parameters: (text uername, text song)
#Returns true if table has been deleted
def remove_playlist(username, song):
    c=db_connect()
    c.execute("Select * from playlist where username = ? and song = ?", (username, song))
    out = 'Successfully deleted the object'
    if(c.fetchone() == None):
        out = 'Username or song does not exist in playlist database'
    c.execute("Delete from playlist where username = ? and song = ?", (username, song))
    c.close()
    db.commit()
    db.close()
    return out

#Takes a username and gives a tuple that contains the songs, artist, and lyrics
#Parameters: (text username)
#Returns a tuple
def user_playlist(username):
    if(check_user(username) == False):
        return('Cannot show a playlist. Username does not exist in user database')
    else:
        c=db_connect()
        c.execute("Select * from playlist where username = ?", (username,))
        try:
            data = c.fetchall()
            songs = []
            artists = []
            lyrics = []
            for i in data:
                songs.append(i[1])
                artists.append(i[2])
                lyrics.append(i[3])
            c.close()
            db.commit()
            db.close()
            return (songs, artists, lyrics)
        except:
            return ('Something is wrong with the playlist')


#tests
'''
create_user('u','p')#user has been successfully created
print(check_user('u'))#true
print(check_user('a'))#false
print(check_pass('u','p'))#true
print(check_pass('u','pa'))#false
add_playlist('ryan', 'abc', 'a', 'abcdefghijklmnopqrstuvwxyz')#Song has not been successfully added. Username does not exist in user database
add_playlist('admin', 'b', 'b', 'b')#Song has successfully been added
print(remove_playlist('admin', 'b'))#Successfully deleted the object
print(remove_playlist('ryan', 'ab'))#Username or song does not exist in playlist database
print(user_playlist('ryan'))#Cannot show a playlist. Username does not exist in user database
print(user_playlist('admin'))#Displays the tuple
'''
#DB MANAGEMENT