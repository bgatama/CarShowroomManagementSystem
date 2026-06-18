from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import mysql.connector

app = Flask(__name__)

@app.route('/')
def template_to_render(): #render the login page
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_to_db():
    # Logic to connect to the database and verify user credentials
    username = request.form['username']
    password = request.form['password']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = %s AND user_password = %s",
                   (username, password))

    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user:
        return render_template('dashboard.html')
    else:
        return render_template('login.html', error="Invalid username or password.")

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='showroom_db'
    )


    
if __name__ == "__main__":
    app.run()