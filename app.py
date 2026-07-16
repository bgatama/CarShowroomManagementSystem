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

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/reports')
def reports():
    return render_template("reports.html")

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

@app.route('/customers')
def customers():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * from customers")

    customers = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("customers.html",
                           customers=customers)

@app.route('/add_customer', methods=['POST'])
def add_customer():
    national_id = request.form['national_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    phone_number = request.form['phone']
    email = request.form['email']
    gender = request.form['gender']
    customer_type = request.form['customer_type']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO customers
        (national_id, first_name, last_name, phone_number, email, gender, customer_type)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (
    national_id,
    first_name,
    last_name,
    phone_number,
    email,
    gender,
    customer_type
    ))

    conn.commit()
    
    cursor.close()
    conn.close()

    return redirect(url_for('customers'))


@app.route('/sales')
def sales():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Customers
    cursor.execute("""
        SELECT customer_id, first_name, last_name
        FROM customers
    """)
    customers = cursor.fetchall()

    # Available vehicles
    cursor.execute("""
        SELECT vehicle_id, make, model
        FROM vehicle
        WHERE vehicle_status='Available'
    """)
    vehicles = cursor.fetchall()

    # Sales table
    cursor.execute("""
        SELECT
            sales.sale_id,
            customers.first_name,
            customers.last_name,
            vehicle.make,
            vehicle.model,
            sales.amount,
            sales.payment_method,
            sales.sale_status,
            sales.sale_date
        FROM sales
        JOIN customers
            ON sales.customer_id = customers.customer_id
        JOIN vehicle
            ON sales.vehicle_id = vehicle.vehicle_id
        ORDER BY sales.sale_date DESC
    """)

    sales = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "sales.html",
        customers=customers,
        vehicles=vehicles,
        sales=sales
    )

@app.route('/add_sale', methods=['POST'])
def add_sale():
    customer_id = request.form['customer_id']
    vehicle_id = request.form['vehicle_id']
    sale_date = request.form['sale_date']
    amount = request.form['amount']
    payment_method = request.form['payment_method']
    sale_status = request.form['sale_status']


    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO sales
        (customer_id, vehicle_id, sale_date, amount, payment_method, sale_status)
        VALUES (%s,%s,%s,%s,%s,%s)
    """,
    (
        customer_id,
        vehicle_id,
        sale_date,
        amount,
        payment_method,
        sale_status
    ))
    conn.commit()

    if sale_status == "Completed":
        cursor.execute("""
            UPDATE vehicle
            SET vehicle_status='Sold'
            WHERE vehicle_id=%s
        """, (vehicle_id,))
        conn.commit()
    
    cursor.close()
    conn.close()

    return redirect(url_for('sales'))

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