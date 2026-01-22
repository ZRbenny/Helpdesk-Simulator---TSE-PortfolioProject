# Helpdesk Simulator

A Technical Solutions Engineer portfolio project demonstrating diagnostic workflows, log analysis, metric-based issue detection, and resolution tracking.

## 🎯 Project Goal

Simulate a TSE workflow for diagnosing production issues:
- View support tickets
- Analyze application logs with filtering
- Review performance metrics with automated issue detection
- Document resolutions in a searchable database
- Build institutional knowledge through a knowledge base

## 🛠️ Tech Stack

- **Backend:** Python 3.x, Flask 2.3.0
- **Database:** SQLite3
- **Frontend:** Jinja2 templates, HTML/CSS
- **Data:** JSON files for ticket/log data
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
│   ├── ticket.html            # Ticket detail page (logs/metrics/resolution form)
│   └── kb.html                # Knowledge base page
│
├── static/                    # CSS stylesheets
│   ├── styles.css             # Global styles (home page, layout)
│   ├── ticket.css             # Ticket detail page styles
│   └── kb.css                 # Knowledge base page styles
│
├── docs/                      # Documentation
│   └── troubleshooting-playbook.md  # TSE methodology guide
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
- **`docs/`** - Documentation and troubleshooting guides

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
git clone https://github.com/ZRbenny/Helpdesk-Simulator---TSE-PortfolioProject.git
cd Helpdesk-Simulator---TSE-PortfolioProject

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

Open browser to `http://localhost:5000`

## ✨ Features Completed

### ✅ Milestone 1-2: Ticket Management
- View list of support tickets with severity indicators
- Click through to individual ticket details
- Display symptoms, reproduction steps, and environment info

### ✅ Milestone 3: Log Analysis
- Parse and display application logs from text files
- Filter by severity level (ERROR, WARN, INFO)
- Color-coded log entries for quick visual scanning
- Monospace font for readability

### ✅ Milestone 4: Metrics & Automated Issue Detection
- Load performance metrics from JSON (response times, error rates, resource usage)
- **Heuristic-based issue detection** using threshold analysis
- Automatic severity classification (CRITICAL, HIGH, MEDIUM)
- Visual highlighting of detected anomalies

**Example Heuristics:**
- Error rate > 5% → HIGH severity
- Redis response time > 100ms → HIGH severity
- Connection timeouts > 0 → CRITICAL severity
- Memory usage > 85% → MEDIUM severity
- Database pool utilization > 90% → CRITICAL severity

### ✅ Milestone 5: Resolution Tracking
- Document root cause analysis, solutions, and prevention strategies
- Store resolutions in SQLite database
- Display resolution history for each ticket
- Form validation and data persistence
- Timestamps and resolver attribution

### ✅ Milestone 6: Knowledge Base
- Searchable knowledge base across all tickets
- View all resolutions in one centralized location
- Search by keyword (root cause, solution, ticket title)
- Links back to original tickets
- Clean, professional interface

## 🎓 TSE Interview Relevance

This project demonstrates key TSE competencies:

1. **Diagnostic Methodology**
   - Systematic approach: Logs → Metrics → Root Cause → Resolution
   - Pattern recognition in error messages and performance data
   - Correlation between symptoms and underlying issues

2. **Tool Building**
   - Created utilities to aid troubleshooting workflows
   - Automated issue detection to reduce manual analysis
   - Built reusable knowledge base

3. **Technical Depth**
   - Understanding of system performance indicators
   - Database design and CRUD operations
   - Web application architecture

4. **Communication & Documentation**
   - Structured resolution documentation
   - Clear presentation of complex technical data
   - Building institutional knowledge

5. **Customer Empathy**
   - Designed intuitive interfaces for non-technical users
   - Focused on actionable insights, not raw data dumps

## 📖 Documentation

**[Troubleshooting Playbook](docs/troubleshooting-playbook.md)** - Step-by-step guide demonstrating how to use this tool to diagnose production issues using TSE methodology. Includes two complete walkthroughs with real examples.

## 📧 Contact

Built by Benny Zarhin as preparation for Technical Solutions Engineer interviews.

GitHub: [@ZRbenny](https://github.com/ZRbenny)