# 🌐 JEMSTAT DATA — Full Project Guide
# Written for: A beginner Python developer learning Computer Science

============================================================
## 📁 PROJECT STRUCTURE (What each file does)
============================================================

jemstat/
│
├── app.py                  ← 🧠 THE BRAIN (Python Flask server)
├── requirements.txt        ← 📦 List of Python packages needed
├── README.txt              ← 📖 This file!
│
├── templates/              ← 🌐 HTML pages (what users see)
│   ├── index.html          ← Customer website (home page)
│   ├── admin.html          ← Your secret dashboard
│   └── admin_login.html    ← Admin login page
│
└── database/               ← 🗄️ Created automatically
    └── orders.db           ← SQLite database (all orders saved here)


============================================================
## 🚀 HOW TO RUN THIS PROJECT
============================================================

STEP 1 — Make sure Python is installed
    Open terminal/command prompt and type:
    python --version
    (Should show Python 3.8 or higher)

STEP 2 — Install Flask (only once)
    pip install flask

STEP 3 — Go into the project folder
    cd jemstat

STEP 4 — Run the server
    python app.py

STEP 5 — Open your browser and visit:
    Website:   http://localhost:5000
    Dashboard: http://localhost:5000/admin
    Password:  jemstat2025


============================================================
## 🧠 HOW THE SYSTEM WORKS (Simple explanation)
============================================================

1. Customer visits the website (index.html)
2. Customer picks a bundle and clicks "Buy Now"
3. Customer enters their phone number
4. Customer clicks "I Have Paid"
5. JavaScript sends the order to Python (using fetch/POST)
6. Python saves the order to the database
7. Python simulates M-Pesa confirming the payment
8. Python sends back: order reference + M-Pesa code
9. Website shows SUCCESS to the customer
10. You (admin) can see all orders in your dashboard


============================================================
## 📚 PYTHON CONCEPTS USED IN THIS PROJECT
============================================================

CONCEPT          | WHERE IT'S USED
-----------------|------------------------------------------
Functions        | def place_order(), def init_db(), etc
Flask Routes     | @app.route("/order", methods=["POST"])
JSON             | request.get_json(), jsonify()
SQLite Database  | sqlite3.connect(), cursor.execute()
String methods   | ''.join(), random.choices()
f-strings        | f"JEM-{random_part}"
If statements    | if not session.get("admin")
Try/Except       | In JavaScript fetch (frontend)
HTTP Methods     | GET (view page) POST (send data)
Sessions         | session["admin"] = True


============================================================
## 🔌 HOW TO MAKE IT REAL (When you are ready)
============================================================

Replace this simulated code in app.py:

    # SIMULATED (current)
    fake_mpesa_code = generate_mpesa_code()

With real Safaricom Daraja API calls:

    # REAL (future)
    # 1. Register at developer.safaricom.co.ke
    # 2. Get Consumer Key + Consumer Secret
    # 3. Use the daraja-python library
    # 4. Receive real M-Pesa callbacks at /mpesa/callback


============================================================
## 🌍 HOW TO HOST THIS ONLINE (Free)
============================================================

1. Create account at render.com
2. Upload this project to GitHub
3. Connect GitHub to Render
4. Render will run your Flask app for free
5. You get a real URL like: https://jemstat-data.onrender.com


============================================================
## 🔐 ADMIN ACCESS
============================================================

URL:      http://localhost:5000/admin
Password: jemstat2025

(Change the password in app.py before going live!)
Look for: if password == "jemstat2025":
Change to: if password == "YOUR_NEW_PASSWORD":


============================================================
## 📞 CONTACT
============================================================

Phone 1: 0716 700 852
Phone 2: 0724 292 415
Business: Jemstat Data

============================================================
## 💡 NEXT THINGS TO LEARN
============================================================

1. Python Flask (you are using it now!)
2. SQLite databases
3. REST APIs (what /order is)
4. HTML + CSS + JavaScript
5. Git & GitHub (to save and share your code)
6. Safaricom Daraja API (for real payments)
7. Deployment (Render, Railway, Heroku)

You are doing great. Keep going! 🔥
