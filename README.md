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
tse-helpdesk/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── data/
│   ├── tickets.json       # Ticket data
│   ├── ticket_001/
│   │   ├── logs.txt       # Application logs
│   │   └── metrics.json   # Performance metrics
│   └── ticket_002/
│       ├── logs.txt
│       └── metrics.json
├── templates/
│   ├── index.html         # Ticket list
│   └── ticket.html        # Ticket detail with logs/metrics
└── static/
    └── styles.css         # Styling
```

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

Built by Benny Zarhin as preparation for Technical Solutions Engineer interviews.