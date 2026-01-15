# Helpdesk Simulator

A Technical Solutions Engineer portfolio project demonstrating diagnostic workflows, log analysis, and metric-based issue detection.

## 🎯 Project Goal

Simulate a TSE workflow for diagnosing production issues:
- View support tickets
- Analyze application logs with filtering
- Review performance metrics
- Identify root causes using automated heuristics
- Document resolutions (coming in Milestone 5)

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **Frontend:** Jinja2 templates, HTML/CSS
- **Data:** JSON files, SQLite (upcoming)
- **Platform:** Windows-compatible, venv-based

## 📁 Project Structure
```
helpdesk-simulator/
├── app.py                      # Flask application with routing and database functions
├── requirements.txt            # Python dependencies
├── resolutions.db             # SQLite database (auto-created, not in Git)
├── .gitignore                 # Git ignore rules
├── README.md                  # Project documentation
│
├── data/                      # Ticket data and diagnostic files
│   ├── tickets.json           # Ticket metadata (ID, title, severity, etc.)
│   ├── ticket_001/
│   │   ├── logs.txt           # Application logs for ticket_001
│   │   └── metrics.json       # Performance metrics for ticket_001
│   └── ticket_002/
│       ├── logs.txt           # Application logs for ticket_002
│       └── metrics.json       # Performance metrics for ticket_002
│
├── templates/                 # Jinja2 HTML templates
│   ├── index.html             # Ticket list page
│   └── ticket.html            # Ticket detail page (logs/metrics/resolution form)
│
├── static/                    # CSS stylesheets
│   ├── styles.css             # Global styles (home page, layout)
│   └── ticket.css             # Ticket detail page styles
│
└── venv/                      # Virtual environment (not in Git)
```

### Key Files

- **`app.py`** - Main Flask application with routes, database functions, and business logic
- **`resolutions.db`** - SQLite database storing resolution history (created automatically on first run)
- **`data/tickets.json`** - Master list of all support tickets
- **`data/ticket_XXX/`** - Each ticket has its own folder containing logs and metrics
- **`templates/`** - HTML templates rendered by Flask with Jinja2
- **`static/`** - CSS files for styling

### Notes

- `resolutions.db` is excluded from Git via `.gitignore` (contains user data)
- `venv/` is excluded from Git (Python virtual environment)
- Each ticket folder follows the naming pattern `ticket_001`, `ticket_002`, etc.


## 💾 Database

The application uses **SQLite** for persistent storage of resolutions.

### Database Schema

**Table: `resolutions`**
```sql
CREATE TABLE resolutions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id TEXT NOT NULL,
    root_cause TEXT NOT NULL,
    solution TEXT NOT NULL,
    prevention TEXT,
    resolved_by TEXT,
    resolved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Auto-Initialization

The database file `resolutions.db` is **automatically created** when you first run the application. The `init_db()` function creates the schema if it doesn't exist.

**Note:** `resolutions.db` is excluded from version control via `.gitignore` as it contains user-generated data.

## 🚀 Setup & Run
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/helpdesk-simulator.git
cd helpdesk-simulator

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

Open browser to `http://localhost:5000`

## ✨ Features

### Milestone 1-2: Ticket Management
- View list of support tickets
- Drill into individual tickets
- Display ticket details (severity, symptoms, environment)

### Milestone 3: Log Analysis
- Parse and display application logs
- Filter by severity level (ERROR, WARN, INFO)
- Color-coded log entries for quick scanning

### Milestone 4: Metrics & Heuristics 
- Load performance metrics (response times, error rates, resource usage)
- **Automated issue detection** using threshold-based heuristics
- Severity classification (CRITICAL, HIGH, MEDIUM)
- Visual highlighting of detected anomalies

### Milestone 5: Resolution Tracking
- Document root cause analysis, solutions, and prevention strategies
- Store resolutions in SQLite database
- Display resolution history for each ticket
- Form validation and data persistence
- Timestamps and resolver attribution

**Example Heuristics:**
- Error rate > 5% → Flag as HIGH
- Redis response time > 100ms → Flag as HIGH
- Connection timeouts > 0 → Flag as CRITICAL
- Memory usage > 85% → Flag as MEDIUM

## 🎓 TSE Interview Relevance

This project demonstrates:
1. **Diagnostic methodology:** Logs → Metrics → Root Cause
2. **Tool building:** Creating utilities to aid troubleshooting
3. **Pattern recognition:** Identifying anomalies in data
4. **Customer empathy:** Designing clear, actionable interfaces
5. **Technical depth:** Understanding system performance indicators

## 📝 Upcoming Features

- **Milestone 6:** Searchable knowledge base
- **Milestone 7:** Interview preparation documentation

Built by Benny Zarhin as preparation for Technical Solutions Engineer interviews..