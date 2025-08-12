from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('internships.db')
    conn.row_factory = sqlite3.Row
    return conn

# Home Page - Show all internships
@app.route('/')
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

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
