def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS applications (
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
    def add_internship(company_name, position, status="Applied", notes="", follow_up_date=""):
        c.execute('''
        INSERT INTO internships (company_name, position, status, notes, follow_up_date)
        VALUES (?, ?, ?, ?, ?)
    ''', (company_name, position, status, notes, follow_up_date))
    conn.commit()
     





    init_db()
    app.run(debug=True)

