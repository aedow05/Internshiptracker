from flask import Flask, render_template, request, redirect
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session, flash
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Set a secret key for session management





# Connect to the SQLite database
def get_db_connection():
    db_path = os.path.abspath('internships.db')
    print(f"Connecting to DB at: {db_path}")
    conn = sqlite3.connect('internships.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    print("Initializing database and creating tables if not exist...")
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
    conn.commit()
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    print("Tables in DB after init:", tables)
    conn.close()
    print("Database initialized.")
init_db()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user is None:
            flash('Incorrect username or password')
        elif not check_password_hash(user['password_hash'], password):
            flash('Incorrect username or password')
        else:
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect('/')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        password_hash = generate_password_hash(password)

        conn = get_db_connection()
        try:
            conn.execute('''
                INSERT INTO users (username, email, password_hash)
                VALUES (?, ?, ?)
            ''', (username, email, password_hash))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return "Username or email already exists", 400
        conn.close()

        return redirect('/login')

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('You need to log in first.')
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function
@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db_connection()
    # Count applications by status
    status_counts = conn.execute('''
        SELECT status, COUNT(*) as count
        FROM applications
        GROUP BY status
    ''').fetchall()

    # Total applications
    total_apps = conn.execute('SELECT COUNT(*) as total FROM applications').fetchone()['total']

    conn.close()
    return render_template('dashboard.html', status_counts=status_counts, total_apps=total_apps, username=session['username'])

    
# Home Page - Show all internships
@app.route('/')
@login_required
def home():
    search = request.args.get('search', '')  # Get search text from query string

    conn = get_db_connection()
    if search:
        applications = conn.execute('''
            SELECT * FROM applications
            WHERE company LIKE ? OR role LIKE ? OR status LIKE ?
        ''', (f'%{search}%', f'%{search}%', f'%{search}%')).fetchall()
    else:
        applications = conn.execute('SELECT * FROM applications').fetchall()
    
    conn.close()
    return render_template('home.html', applications=applications, search=search)


# Add New Internship
@app.route('/add', methods=['GET', 'POST'])
def add_internship():
    if request.method == 'POST':
        company = request.form['company']
        role = request.form['role']
        date_applied = request.form['date_applied']
        job_link = request.form['job_link']
        status = request.form['status']
        notes = request.form['notes']
        follow_up_date = request.form['follow_up_date']

        conn = get_db_connection()
        conn.execute('''
            INSERT INTO applications (company, role, date_applied, job_link, status, notes, follow_up_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (company, role, date_applied, job_link, status, notes, follow_up_date))
        conn.commit()
        conn.close()
        return redirect('/')
    
    return render_template('add_internship.html')

# Edit Internship
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_internship(id):
    conn = get_db_connection()
    app_data = conn.execute('SELECT * FROM applications WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        company = request.form['company']
        role = request.form['role']
        date_applied = request.form['date_applied']
        job_link = request.form['job_link']
        status = request.form['status']
        notes = request.form['notes']
        follow_up_date = request.form['follow_up_date']

        conn.execute('''
            UPDATE applications
            SET company = ?, role = ?, date_applied = ?, job_link = ?, status = ?, notes = ?, follow_up_date = ?
            WHERE id = ?
        ''', (company, role, date_applied, job_link, status, notes, follow_up_date, id))
        conn.commit()
        conn.close()
        return redirect('/')

    conn.close()
    return render_template('edit_internship.html', app=app_data)

# Delete Internship
@app.route('/delete/<int:id>')
def delete_internship(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM applications WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')
@app.route('/internships')
def list_internships():
    conn = get_db_connection()
    internships = conn.execute("SELECT * FROM internships ORDER BY start_date DESC").fetchall()
    conn.close()
    return render_template('internships.html', internships=internships)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
