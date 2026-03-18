import os
import sqlite3
from datetime import datetime

from flask import (Flask, g, redirect, render_template, request, session,
                   url_for, flash)
from werkzeug.security import check_password_hash, generate_password_hash

from models.anomaly import detect_anomaly

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "energy.db")

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")
app.config["DATABASE"] = DATABASE_PATH


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()
    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS energy (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            device_name TEXT NOT NULL,
            units REAL NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );
        """
    )
    db.commit()


@app.before_request
def load_logged_in_user():
    init_db()
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = get_user_by_id(user_id)


@app.teardown_appcontext
def teardown_db(exception):
    close_db(exception)


def get_user_by_id(user_id):
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    return user


def get_user_by_username(username):
    db = get_db()
    return db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()


def login_required(view):
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("login"))
        return view(**kwargs)

    wrapped_view.__name__ = view.__name__
    return wrapped_view


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Username and password are required.", "error")
            return render_template("register.html")

        if get_user_by_username(username) is not None:
            flash("That username is already registered.", "error")
            return render_template("register.html")

        hashed = generate_password_hash(password)
        db = get_db()
        db.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed),
        )
        db.commit()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        error = None

        user = get_user_by_username(username)
        if user is None:
            error = "Incorrect username or password."
        elif not check_password_hash(user["password"], password):
            error = "Incorrect username or password."

        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("dashboard"))

        flash(error, "error")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


def get_energy_entries(user_id):
    db = get_db()
    return db.execute(
        "SELECT * FROM energy WHERE user_id = ? ORDER BY datetime(timestamp) ASC",
        (user_id,),
    ).fetchall()


def add_energy_entry(user_id, device_name, units, timestamp):
    db = get_db()
    db.execute(
        "INSERT INTO energy (user_id, device_name, units, timestamp) VALUES (?, ?, ?, ?)",
        (user_id, device_name, units, timestamp),
    )
    db.commit()


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    if request.method == "POST":
        device = request.form.get("device_name", "").strip()
        units = request.form.get("units", "")
        timestamp = request.form.get("timestamp", datetime.utcnow().isoformat())

        error = None
        try:
            units_value = float(units)
        except ValueError:
            units_value = None

        if not device:
            error = "Device name is required."
        elif units_value is None or units_value < 0:
            error = "Please enter a valid number of units."

        if error:
            flash(error, "error")
        else:
            add_energy_entry(g.user["id"], device, units_value, timestamp)
            flash("Energy record added.", "success")
            return redirect(url_for("dashboard"))

    entries = get_energy_entries(g.user["id"])

    total_usage = sum([entry["units"] for entry in entries])

    device_totals = {}
    for entry in entries:
        device_totals.setdefault(entry["device_name"], 0)
        device_totals[entry["device_name"]] += entry["units"]

    # Anomaly detection (Smart Grid Cybersecurity + Fault Detection)
    alerts = []
    prev_values = {}
    last_units_overall = None

    for entry in entries:
        device = entry["device_name"]
        units = entry["units"]
        prev = prev_values.get(device)

        # If there is no prior usage for this device, fall back to overall last units
        # to help detect sudden spikes across devices (cyber threat).
        if prev is None:
            prev = last_units_overall

        status = detect_anomaly(units, prev)
        if status == "fault":
            alerts.append({
                "type": "fault",
                "device": device,
                "units": units,
                "message": "⚠️ Possible device malfunction detected",
                "timestamp": entry["timestamp"],
            })
        elif status == "cyber_threat":
            alerts.append({
                "type": "cyber_threat",
                "device": device,
                "units": units,
                "message": "🚨 Potential cyber threat detected",
                "timestamp": entry["timestamp"],
            })

        prev_values[device] = units
        last_units_overall = units

    # Ensure latest alerts are shown first
    alerts = sorted(alerts, key=lambda a: a["timestamp"], reverse=True)
    latest_alerts = alerts[:5]

    # Build chart data
    chart_labels = [entry["timestamp"] for entry in entries]
    chart_data = [entry["units"] for entry in entries]

    suggestions = []
    if total_usage > 0:
        suggestions.append("Check your most-used devices and consider powering them off when idle.")
        if any(a["type"] == "fault" for a in alerts):
            suggestions.append("Inspect devices that are showing unusually high usage.")
        if any(a["type"] == "cyber_threat" for a in alerts):
            suggestions.append("Review network-connected devices for unexpected activity.")

    return render_template(
        "dashboard.html",
        total_usage=total_usage,
        device_totals=device_totals,
        alerts=alerts,
        chart_labels=chart_labels,
        chart_data=chart_data,
        suggestions=suggestions,
        entries=entries,
    )


if __name__ == "__main__":
    app.run(debug=True)
