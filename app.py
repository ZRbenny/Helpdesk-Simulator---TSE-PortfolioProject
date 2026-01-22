from flask import Flask, render_template, abort
import json
from pathlib import Path
import sqlite3
from datetime import datetime

app = Flask(__name__)

DATA_DIR = Path(__file__).parent / "data"
TICKETS_FILE = DATA_DIR / "tickets.json"


def load_tickets():
    """Load tickets with graceful error handling."""
    try:
        with open(TICKETS_FILE, "r", encoding="utf-8") as f:
            return json.load(f) 
    except FileNotFoundError:
        print(f"WARNING: {TICKETS_FILE} not found")
        return []
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in tickets.json: {e}")
        return []

def load_logs(ticket_id, level_filter=None):
    """
    Load logs for a ticket with optional severity filtering.
    
    Args:
        ticket_id: The ticket ID (e.g., 'ticket_001')
        level_filter: Optional severity level ('ERROR', 'WARN', 'INFO', or None for all)
    
    Returns:
        List of dictionaries with parsed log entries
    """
    log_file = DATA_DIR / ticket_id / "logs.txt"
    
    # Handle missing log files gracefully
    if not log_file.exists():
        return []
    
    logs = []
    
    try:
        with open(log_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:  # Skip empty lines
                    continue
                
                # Parse log line: "2024-01-10 14:28:45 INFO [Service] Message"
                parts = line.split(maxsplit=3)  # Split into 4 parts max
                
                if len(parts) < 4:
                    continue  # Skip malformed lines
                
                date, time, level, message = parts
                
                # Apply filter if specified
                if level_filter and level != level_filter:
                    continue
                
                logs.append({
                    "timestamp": f"{date} {time}",
                    "level": level,
                    "message": message
                })

    except Exception as e:
        print(f"ERROR loading logs for {ticket_id}: {e}")
        return []
    
    return logs

def load_metrics(ticket_id):
    """
    Load performance metrics for a ticket.
    
    Returns:
        Dictionary of metrics or empty dict if file missing
    """
    metrics_file = DATA_DIR / ticket_id / "metrics.json"
    
    if not metrics_file.exists():
        return {}
    
    try:
        with open(metrics_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"ERROR loading metrics for {ticket_id}: {e}")
        return {}


def analyze_metrics(metrics):
    """
    Apply heuristics to detect issues in metrics.
    
    Returns:
        List of dictionaries with detected issues
    """
    issues = []
    
    # Check authentication service
    if "authentication_service" in metrics:
        auth = metrics["authentication_service"]
        
        if auth.get("error_rate_percent", 0) > 5:
            issues.append({
                "severity": "high",
                "component": "Authentication Service",
                "issue": f"Error rate is {auth['error_rate_percent']}% (threshold: 5%)",
                "metric": "error_rate_percent"
            })
        
        if auth.get("avg_response_time_ms", 0) > 500:
            issues.append({
                "severity": "medium",
                "component": "Authentication Service",
                "issue": f"Slow response time: {auth['avg_response_time_ms']}ms (threshold: 500ms)",
                "metric": "avg_response_time_ms"
            })
    
    # Check Redis connection
    if "redis_connection" in metrics:
        redis = metrics["redis_connection"]
        
        if redis.get("avg_response_time_ms", 0) > 100:
            issues.append({
                "severity": "high",
                "component": "Redis Connection",
                "issue": f"Very slow response: {redis['avg_response_time_ms']}ms (threshold: 100ms)",
                "metric": "avg_response_time_ms"
            })
        
        if redis.get("timeout_count", 0) > 0:
            issues.append({
                "severity": "critical",
                "component": "Redis Connection",
                "issue": f"{redis['timeout_count']} connection timeouts detected",
                "metric": "timeout_count"
            })
    
    # Check dashboard service
    if "dashboard_service" in metrics:
        dash = metrics["dashboard_service"]
        
        if dash.get("avg_response_time_ms", 0) > 3000:
            issues.append({
                "severity": "high",
                "component": "Dashboard Service",
                "issue": f"Very slow response: {dash['avg_response_time_ms']}ms (threshold: 3000ms)",
                "metric": "avg_response_time_ms"
            })
    
    # Check database queries
    if "database_queries" in metrics:
        db = metrics["database_queries"]
        
        if db.get("avg_query_time_ms", 0) > 1000:
            issues.append({
                "severity": "high",
                "component": "Database Queries",
                "issue": f"Slow query performance: {db['avg_query_time_ms']}ms avg (threshold: 1000ms)",
                "metric": "avg_query_time_ms"
            })
    
    # Check resource utilization
    if "server_resources" in metrics:
        res = metrics["server_resources"]
        
        if res.get("memory_percent", 0) > 85:
            issues.append({
                "severity": "medium",
                "component": "Server Resources",
                "issue": f"High memory usage: {res['memory_percent']}% (threshold: 85%)",
                "metric": "memory_percent"
            })
        
        if res.get("disk_io_percent", 0) > 80:
            issues.append({
                "severity": "high",
                "component": "Server Resources",
                "issue": f"High disk I/O: {res['disk_io_percent']}% (threshold: 80%)",
                "metric": "disk_io_percent"
            })
    
    # Check database pool
    if "database_pool" in metrics:
        pool = metrics["database_pool"]
        
        if pool.get("pool_utilization_percent", 0) > 90:
            issues.append({
                "severity": "critical",
                "component": "Database Pool",
                "issue": f"Connection pool nearly exhausted: {pool['pool_utilization_percent']}% (threshold: 90%)",
                "metric": "pool_utilization_percent"
            })
    
    return issues


def init_db():
    """Initialize the SQLite database with resolutions table."""
    conn = sqlite3.connect('resolutions.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resolutions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id TEXT NOT NULL,
            root_cause TEXT NOT NULL,
            solution TEXT NOT NULL,
            prevention TEXT,
            resolved_by TEXT,
            resolved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()


def save_resolution(ticket_id, root_cause, solution, prevention, resolved_by):
    """
    Save a resolution to the database.
    
    Returns:
        True if successful, False otherwise
    """
    try:
        conn = sqlite3.connect('resolutions.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO resolutions (ticket_id, root_cause, solution, prevention, resolved_by)
            VALUES (?, ?, ?, ?, ?)
        ''', (ticket_id, root_cause, solution, prevention, resolved_by))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"ERROR saving resolution: {e}")
        return False


def get_resolutions(ticket_id):
    """
    Get all resolutions for a specific ticket.
    
    Returns:
        List of resolution dictionaries
    """
    try:
        conn = sqlite3.connect('resolutions.db')
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM resolutions 
            WHERE ticket_id = ? 
            ORDER BY resolved_at DESC
        ''', (ticket_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        # Convert to list of dictionaries
        return [dict(row) for row in rows]
    except Exception as e:
        print(f"ERROR loading resolutions: {e}")
        return []

#home page showing list of tickets
@app.route("/")
def home():
    tickets = load_tickets()
    return render_template("index.html", tickets=tickets)



#ticket detail page showing logs for a specific ticket
@app.route("/tickets/<ticket_id>", methods=["GET", "POST"])
def ticket_detail(ticket_id):
    from flask import request, redirect, url_for
    
    tickets = load_tickets()
    ticket = next((t for t in tickets if t.get("id") == ticket_id), None)
    
    if ticket is None:
        abort(404)
    
    # Handle resolution form submission
    if request.method == "POST":
        root_cause = request.form.get("root_cause", "").strip()
        solution = request.form.get("solution", "").strip()
        prevention = request.form.get("prevention", "").strip()
        resolved_by = request.form.get("resolved_by", "").strip()
        
        # Validate required fields
        if root_cause and solution and resolved_by:
            success = save_resolution(ticket_id, root_cause, solution, prevention, resolved_by)
            if success:
                # Redirect to same page to prevent form resubmission
                return redirect(url_for('ticket_detail', ticket_id=ticket_id))
        else:
            # Could add error handling here
            pass
    
    # Load data for display
    level_filter = request.args.get("level")
    logs = load_logs(ticket_id, level_filter)
    metrics = load_metrics(ticket_id)
    issues = analyze_metrics(metrics) if metrics else []
    resolutions = get_resolutions(ticket_id)
    
    return render_template(
        "ticket.html", 
        ticket=ticket, 
        logs=logs, 
        current_filter=level_filter,
        metrics=metrics,
        issues=issues,
        resolutions=resolutions
    )

#Loads knowledge base page showing all resolutions
@app.route("/kb")
def knowledge_base():
    """Knowledge base page showing all resolutions across all tickets."""
    from flask import request
    
    # Get search query if provided
    search_query = request.args.get("q", "").strip().lower()
    
    try:
        conn = sqlite3.connect('resolutions.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get all resolutions with ticket info
        cursor.execute('''
            SELECT * FROM resolutions 
            ORDER BY resolved_at DESC
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        # Convert to list of dictionaries and add ticket titles
        all_resolutions = []
        tickets = load_tickets()
        ticket_map = {t['id']: t for t in tickets}  # Create lookup dictionary
        
        for row in rows:
            resolution = dict(row)
            # Add ticket title for display
            ticket = ticket_map.get(resolution['ticket_id'], {})
            resolution['ticket_title'] = ticket.get('title', 'Unknown Ticket')
            
            # Filter by search query if provided
            if search_query:
                searchable_text = (
                    resolution['root_cause'].lower() + " " +
                    resolution['solution'].lower() + " " +
                    resolution.get('prevention', '').lower() + " " +
                    resolution['ticket_title'].lower()
                )
                
                if search_query in searchable_text:
                    all_resolutions.append(resolution)
            else:
                all_resolutions.append(resolution)
        
        return render_template(
            "kb.html",
            resolutions=all_resolutions,
            search_query=search_query,
            total_count=len(all_resolutions)
        )
        
    except Exception as e:
        print(f"ERROR loading knowledge base: {e}")
        return render_template("kb.html", resolutions=[], search_query="", total_count=0)
    
if __name__ == "__main__":
    # Initialize database on startup
    init_db()
    print("Database initialized")
    
    app.run(debug=True, port=5000)



