import sqlite3
#rename maybe for playlist pizzaz

DB_FILE = "database.db"

db = None
db = sqlite3.connect(DB_FILE, check_same_thread = False)
c = db.cursor()

db.executescript("""
CREATE TABLE if not exists users(username text, password text);
Insert into users values(?,?), ('Ryan', 'password');
""")

def db_connect():
    global db
    db = sqlite3.connect(DB_FILE)
    return db.cursor()

#Creates a new user.
#Parameters: (text username, text password)
#Returns nothing
def create_user(username, password):
    c=db_connect()
    c.execute("Insert into users values(?,?)", (username, password))
    c.close()
    db.close()

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

print(create_user('u','p'))
print(check_user('u'))
print(check_pass('u','p'))
#DB MANAGEMENT

