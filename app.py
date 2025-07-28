from flask import Flask
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('internships.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    conn = get_db_connection()
    applications = conn.execute('SELECT * FROM applications').fetchall()
    conn.close()

    # Build HTML response
    html = "<h1>Internship Applications</h1><ul>"
    for app in applications:
        html += f"<li><strong>{app['company']}</strong> - {app['role']} ({app['status']})</li>"
    html += "</ul>"

    return html

if __name__ == '__main__':
    app.run(debug=True)
