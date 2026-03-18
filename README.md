# Cyber-Resilient Smart Energy System

A simple full-stack Flask web application to monitor energy usage, detect faulty devices, and identify cyber threats using basic anomaly detection.

## 🚀 Features

- User registration, login, and logout (session-based auth)
- Add energy usage records by device
- Fault detection (high usage)
- Cyber threat detection (sudden spikes)
- Dashboard with bold UI, stats, alerts, and charts

## 🛠️ Installation

1. Clone or download this repository.
2. Create a Python virtual environment (recommended):

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

3. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

4. Start the app:

```bash
python app.py
```

5. Open `http://127.0.0.1:5000` in your browser.

## 🗂️ Project Structure

- `app.py` – Main Flask application
- `models/anomaly.py` – Simple anomaly detection logic
- `templates/` – HTML templates for UI
- `static/` – CSS and JavaScript assets
- `energy.db` – SQLite database (created automatically)

## ✅ Notes

- The database file `energy.db` is created automatically in the project root.
- Modify the `THRESHOLD` constant in `models/anomaly.py` to adjust fault detection sensitivity.
