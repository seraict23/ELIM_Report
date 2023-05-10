import sqlite3

con = sqlite3.connect('db.sqlite3')

cursor = con.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())

cursor.execute("SELECT * FROM 'common_common'")
print(cursor.fetchall())
