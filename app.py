from flask_login import login_user, logout_user, login_required, current_user
from datetime import date

from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = "expense_tracker_secret_key"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

DB_NAME = "database.db"


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()
    conn.close()

    if user:
        return User(user["id"], user["username"], user["password"])
    return None


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        type TEXT,
        amount REAL,
        category TEXT,
        description TEXT,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            login_user(User(user["id"], user["username"], user["password"]))
            return redirect(url_for("dashboard"))

        return "Invalid username or password"

    return render_template("login.html")



@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        try:
            conn = get_db_connection()
            conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed_password)
            )
            conn.commit()
            conn.close()
            return redirect(url_for("login"))
        except:
            return "Username already exists"

    return render_template("register.html")

@app.route("/dashboard")
@login_required
def dashboard():
    conn = get_db_connection()

    income = conn.execute("""
        SELECT SUM(amount) FROM transactions
        WHERE user_id = ? AND type = 'income'
    """, (current_user.id,)).fetchone()[0] or 0

    expense = conn.execute("""
        SELECT SUM(amount) FROM transactions
        WHERE user_id = ? AND type = 'expense'
    """, (current_user.id,)).fetchone()[0] or 0

    transactions = conn.execute("""
        SELECT * FROM transactions
        WHERE user_id = ?
        ORDER BY date DESC
        LIMIT 5
    """, (current_user.id,)).fetchall()

    conn.close()

    balance = income - expense

    return render_template(
        "dashboard.html",
        income=income,
        expense=expense,
        balance=balance,
        transactions=transactions
    )


@app.route("/add", methods=["GET", "POST"])
@login_required
def add_transaction():
    if request.method == "POST":
        t_type = request.form["type"]
        amount = float(request.form["amount"])
        category = request.form["category"]
        description = request.form["description"]
        today = date.today().isoformat()

        conn = get_db_connection()
        conn.execute("""
            INSERT INTO transactions (user_id, type, amount, category, description, date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (current_user.id, t_type, amount, category, description, today))
        conn.commit()
        conn.close()

        return redirect(url_for("dashboard"))

    return render_template("add_transaction.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


if __name__ == "__main__":
    init_db()
    app.run()
