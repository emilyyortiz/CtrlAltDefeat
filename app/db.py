import sqlite3
#rename maybe for playlist pizzaz

DB_FILE = "database.db"

db = None
db = sqlite3.connect(DB_FILE)
c = db.cursor()

#DB MANAGEMENT