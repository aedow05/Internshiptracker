import sqlite3

conn = sqlite3.connect('internships.db')
c = conn.cursor()

c.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = c.fetchall()

print("Tables in database:", tables)

conn.close()
