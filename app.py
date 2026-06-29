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
        return render_template('login.html', error="Invalid username or password")


def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='showroom_db'
    )

#Various routes for different pages
@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

@app.route('/customers')
def customers():
    return render_template("customers.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/reports')
def reports():
    return render_template("reports.html")

@app.route('/sales')
def sales():
    return render_template("sales.html")

@app.route('/vehicles')
def vehicles():
    return render_template("vehicles.html")

    
if __name__ == "__main__":
    app.run()