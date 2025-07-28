import sqlite3

conn = sqlite3.connect('internships.db')
c = conn.cursor()

# Sample data
sample_data = [
    ('Google', 'Software Intern', '2025-06-01', 'https://careers.google.com', 'Applied', 'Excited about this one', '2025-06-15'),
    ('Meta', 'Backend Intern', '2025-06-03', 'https://www.metacareers.com', 'Applied', '', '2025-06-18'),
    ('Netflix', 'Data Analyst Intern', '2025-06-05', '', 'Interview Scheduled', 'Second round next week', '2025-06-20'),
]

c.executemany('''
    INSERT INTO applications (company, role, date_applied, job_link, status, notes, follow_up_date)
    VALUES (?, ?, ?, ?, ?, ?, ?)
''', sample_data)

conn.commit()
conn.close()
print("Sample data inserted successfully.")
