# ============================================================
#  JEMSTAT DATA - Main Backend Server
#  Built with Python Flask
#
#  WHAT IS THIS FILE?
#  This is the "brain" of the website. It:
#  1. Serves web pages to visitors
#  2. Receives orders from the website
#  3. Simulates M-Pesa payment confirmation
#  4. Stores orders in a database
#  5. Shows an admin dashboard to you (the owner)
#
#  PYTHON CONCEPTS YOU WILL LEARN HERE:
#  - Flask (web framework)
#  - Routes (URLs that do things)
#  - Functions
#  - JSON (data format used by APIs)
#  - SQLite (simple database)
# ============================================================

from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from datetime import datetime
import sqlite3
import random
import string
import os

# --- Create the Flask app ---
# Think of this like turning on the website engine
app = Flask(__name__)
app.secret_key = "jemstat_secret_2025"  # Used to protect admin login

# --- Database file location ---
DB_PATH = "database/orders.db"

# ============================================================
#  DATABASE SETUP
#  SQLite is a simple database stored in one file.
#  Perfect for learning - no complicated setup needed!
# ============================================================

def init_db():
    """
    WHAT IS THIS?
    A function that creates our database tables when the app starts.
    Think of a table like an Excel spreadsheet with rows and columns.
    """
    os.makedirs("database", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create the orders table
    # Each order has: id, customer phone, bundle, amount, status, date
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_ref TEXT UNIQUE,
            phone TEXT NOT NULL,
            bundle_name TEXT NOT NULL,
            bundle_size TEXT NOT NULL,
            amount INTEGER NOT NULL,
            validity TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            mpesa_code TEXT,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def generate_order_ref():
    """
    WHAT IS THIS?
    Generates a unique order reference like 'JEM-A3X9K'
    random.choices picks random letters/numbers
    ''.join combines them into one string
    """
    chars = string.ascii_uppercase + string.digits
    random_part = ''.join(random.choices(chars, k=5))
    return f"JEM-{random_part}"

def generate_mpesa_code():
    """
    Simulates a fake M-Pesa transaction code like 'QHX72ABDKE'
    In real life, M-Pesa sends this automatically.
    """
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=10))

# ============================================================
#  ROUTES - These are the URLs of your website
#  @app.route("/something") means:
#  "When someone visits /something, run this function"
# ============================================================

# --- HOME PAGE ---
@app.route("/")
def home():
    """Shows the main website to customers"""
    return render_template("index.html")

# --- PLACE ORDER ---
# This runs when a customer clicks "I Have Paid - Send Bundle"
@app.route("/order", methods=["POST"])
def place_order():
    """
    WHAT HAPPENS HERE:
    1. We receive the customer's order data (JSON)
    2. We save it to the database as 'pending'
    3. We simulate M-Pesa confirming the payment
    4. We update the order to 'confirmed'
    5. We send back a success message

    In REAL life, step 3 would be replaced by:
    - Waiting for Safaricom to send us a payment notification
    - Verifying the payment is real
    - Then sending the actual bundle via Safaricom API
    """

    # Get the data sent from the website (JSON format)
    data = request.get_json()

    # Extract each piece of information
    phone     = data.get("phone")
    bundle    = data.get("bundle")
    size      = data.get("size")
    amount    = data.get("amount")
    validity  = data.get("validity")

    # Basic validation - make sure nothing is empty
    if not all([phone, bundle, size, amount, validity]):
        return jsonify({"success": False, "message": "Missing order details"}), 400

    # Generate a unique reference for this order
    order_ref = generate_order_ref()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Save order to database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO orders (order_ref, phone, bundle_name, bundle_size, amount, validity, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, 'pending', ?)
    """, (order_ref, phone, bundle, size, amount, validity, now))
    conn.commit()

    # ---- SIMULATED M-PESA CONFIRMATION ----
    # In real life: Safaricom sends a callback to /mpesa/callback
    # For now: we simulate it happening automatically
    fake_mpesa_code = generate_mpesa_code()
    cursor.execute("""
        UPDATE orders SET status='confirmed', mpesa_code=?
        WHERE order_ref=?
    """, (fake_mpesa_code, order_ref))
    conn.commit()
    conn.close()

    # Send success response back to the website
    return jsonify({
        "success": True,
        "order_ref": order_ref,
        "mpesa_code": fake_mpesa_code,
        "message": f"Bundle confirmed! Reference: {order_ref}"
    })

# --- REAL M-PESA CALLBACK (for future use) ---
@app.route("/mpesa/callback", methods=["POST"])
def mpesa_callback():
    """
    FUTURE USE:
    When you register with Safaricom Daraja API,
    Safaricom will call THIS URL automatically every time
    someone pays you via M-Pesa.

    You give Safaricom this URL and they send payment data here.
    This is called a "webhook" - very common in real systems!
    """
    data = request.get_json()
    # TODO: Parse Safaricom payment data and confirm order
    # This is where real automation happens
    return jsonify({"ResultCode": 0, "ResultDesc": "Success"})

# --- ADMIN LOGIN ---
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    """Simple admin login to protect your dashboard"""
    if request.method == "POST":
        password = request.form.get("password")
        # In real life, use a proper hashed password!
        if password == "jemstat2025":
            session["admin"] = True
            return redirect(url_for("admin_dashboard"))
        return render_template("admin_login.html", error="Wrong password!")
    return render_template("admin_login.html")

# --- ADMIN DASHBOARD ---
@app.route("/admin")
def admin_dashboard():
    """
    Shows you all orders, revenue, and stats.
    Only accessible if you are logged in as admin.
    """
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Makes rows accessible like dictionaries
    cursor = conn.cursor()

    # Get all orders (newest first)
    cursor.execute("SELECT * FROM orders ORDER BY id DESC")
    orders = cursor.fetchall()

    # Calculate stats
    cursor.execute("SELECT COUNT(*) FROM orders WHERE status='confirmed'")
    total_orders = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(amount) FROM orders WHERE status='confirmed'")
    total_revenue = cursor.fetchone()[0] or 0

    cursor.execute("SELECT COUNT(*) FROM orders WHERE status='pending'")
    pending_count = cursor.fetchone()[0]

    conn.close()

    return render_template("admin.html",
        orders=orders,
        total_orders=total_orders,
        total_revenue=total_revenue,
        pending_count=pending_count
    )

# --- ADMIN LOGOUT ---
@app.route("/admin/logout")
def admin_logout():
    session.clear()
    return redirect(url_for("home"))

# --- CHECK ORDER STATUS ---
@app.route("/order/status/<order_ref>")
def order_status(order_ref):
    """Customer can check their order status"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE order_ref=?", (order_ref,))
    order = cursor.fetchone()
    conn.close()

    if not order:
        return jsonify({"found": False})

    return jsonify({
        "found": True,
        "order_ref": order["order_ref"],
        "status": order["status"],
        "bundle": order["bundle_name"],
        "amount": order["amount"],
        "mpesa_code": order["mpesa_code"],
        "created_at": order["created_at"]
    })

# ============================================================
#  START THE APP
#  debug=True means the server restarts automatically
#  when you change the code - very useful when learning!
# ============================================================
if __name__ == "__main__":
    init_db()  # Create database tables
    print("=" * 50)
    print("  JEMSTAT DATA SERVER STARTING...")
    print("  Open: http://localhost:5000")
    print("  Admin: http://localhost:5000/admin")
    print("  Admin password: jemstat2025")
    print("=" * 50)
    app.run(debug=True, port=5000)
