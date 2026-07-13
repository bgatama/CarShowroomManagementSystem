from flask import Flask, render_template, request, redirect, url_for
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
        return calculate_totals()
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
    return calculate_totals()

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
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * from `vehicle`" )

    vehicles = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("vehicles.html",
                           vehicles=vehicles
                           )



@app.route('/add_vehicle', methods=['POST'])
def add_vehicle():
    make = request.form['make']
    model = request.form['model']
    year = request.form['year']
    price = request.form['price']
    vehicle_vin_number = request.form['vehicle_vin_number']
    purchase_date = request.form['purchase_date']
    vehicle_status = request.form['vehicle_status']

    conn = get_db_connection()
    cursor = conn.cursor()


    cursor.execute("""
INSERT INTO vehicle (make, model, year, vehicle_vin_number, price, vehicle_status, purchase_date)
                  values (%s,%s,%s,%s,%s,%s,%s)
                  """,
                (
                    make,
                    model,
                    year,
                    vehicle_vin_number,
                    price,
                    vehicle_status,
                    purchase_date
                )
                  )
    
    conn.commit()

    
    cursor.close()
    conn.close()

    return redirect(url_for('vehicles'))


#Function for calculating the total vehicles, sales, customers and getting the revenue
def calculate_totals():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM vehicle")
    total_vehicles = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM customers")
    total_customers = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM sales")
    total_sales = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(amount) FROM sales")
    total_revenue = cursor.fetchone()[0] or 0

    cursor.close()
    conn.close()

    return render_template(
        "dashboard.html",
        total_vehicles=total_vehicles,
        total_customers=total_customers,
        total_sales=total_sales,
        total_revenue=total_revenue
    )



 
if __name__ == "__main__":
    app.run()