import sqlite3

# Connect to the database
conn = sqlite3.connect('internships.db')
c = conn.cursor()

# Drop the table if it already exists (optional, for testing)
c.execute('DROP TABLE IF EXISTS applications')

# Create the applications table
c.execute('''
    CREATE TABLE applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT NOT NULL,
        role TEXT NOT NULL,
        date_applied TEXT,
        job_link TEXT,
        status TEXT,
        notes TEXT,
        follow_up_date TEXT
    )
''')

# Insert sample data
sample_data = [
    ('OpenAI', 'ML Intern', '2025-07-27', 'https://openai.com/careers', 'Applied', 'Excited about this role', '2025-08-05'),
    ('Google', 'Software Intern', '2025-07-26', 'https://careers.google.com', 'Interviewing', 'Had phone screen', '2025-08-02'),
    ('Microsoft', 'Data Science Intern', '2025-07-25', 'https://careers.microsoft.com', 'Rejected', 'No reply yet', '2025-08-01'),
]

c.executemany('''
    INSERT INTO applications (company, role, date_applied, job_link, status, notes, follow_up_date)
    VALUES (?, ?, ?, ?, ?, ?, ?)
''', sample_data)

# Commit and close
conn.commit()
conn.close()
print("Database initialized with sample data.")
