<<<<<<< HEAD
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
=======
⚡ Cyber-Resilient Smart Energy System

A full-stack web application that monitors energy consumption, detects faulty devices, and identifies potential cyber threats using anomaly detection.

🚀 Project Overview

This project focuses on building a **smart and secure energy monitoring system** that ensures:

- Cybersecurity in smart energy systems
- Fault detection and predictive maintenance
- Real-time energy monitoring and visualization

##  Key Features

- Smart Grid Cybersecurity

* Detects sudden spikes in energy usage
* Identifies suspicious patterns
* Raises alerts for potential cyber threats

- Fault Detection & Predictive Maintenance

* Detects abnormal energy consumption
* Identifies potentially faulty devices
* Provides early warnings to prevent failures

📊 Dashboard

* Total energy usage
* Devices tracked
* Alerts count (Cyber threats & Faults)
* Energy usage trends (Chart.js)
* Energy history table

 🚨 Alert System

* 🚨 Cyber Threat Alerts (Red)
* ⚠️ Fault Alerts (Yellow)
* Real-time alert display

 💡 Optimization Tips

* Suggests reducing energy usage
* Recommends checking faulty devices


##  Installation & Setup

### 1️⃣ Clone the repository

```
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2️⃣ Install dependencies

```
pip install -r requirements.txt
```

### 3️⃣ Run the application

```
python app.py
```

### 4️⃣ Open in browser

```
http://127.0.0.1:5000/
```


## 🧪 How It Works

1. User logs into the system
2. Adds energy data (device + units)
3. System compares with previous data
4. Detects:

   * ⚠️ Fault → High usage
   * 🚨 Cyber Threat → Sudden spike
5. Alerts are displayed on dashboard


---

## 📜 License

This project is for educational and hackathon purposes.
>>>>>>> 2d81d55cb3b52facd5a067914c9d22e7a99cf29a
