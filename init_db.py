import sqlite3

conn = sqlite3.connect('internships.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT NOT NULL,
    role TEXT NOT NULL,
    date_applied DATE,
    job_link TEXT,
    status TEXT NOT NULL,
    notes TEXT,
    follow_up_date DATE
)
''')

conn.commit()
conn.close()
print("Database initialized.")
