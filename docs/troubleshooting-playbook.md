# Troubleshooting Playbook

This document demonstrates how to use the Helpdesk Simulator to diagnose and resolve production issues using a systematic TSE methodology.

---

## General Diagnostic Workflow
```
1. Review Ticket → 2. Check Metrics → 3. Analyze Logs → 4. Identify Root Cause → 5. Document Resolution
```

---

## Example 1: Diagnosing Intermittent Login Failures (ticket_001)

### Step 1: Review the Ticket
- **Symptoms:** Users get "Invalid session" errors and forced to re-login repeatedly
- **Severity:** High
- **Environment:** Production-like, Chrome/Edge, Windows

### Step 2: Check Auto-Detected Issues
Navigate to the ticket and review the Performance Metrics section:

**Issues Flagged:**
- 🔴 **CRITICAL:** Redis Connection - 8 connection timeouts detected
- 🟡 **HIGH:** Redis Connection - Very slow response: 1250ms (threshold: 100ms)
- 🟡 **HIGH:** Authentication Service - Error rate is 7.69% (threshold: 5%)
- 🔵 **MEDIUM:** Server Resources - High memory usage: 89% (threshold: 85%)

**Initial Hypothesis:** Redis infrastructure issue causing session validation failures

### Step 3: Analyze Logs
Filter logs by severity:
1. Click **ERROR** filter
2. Observe pattern:
   - Multiple "Session validation failed: token mismatch" errors
   - "Failed to persist session to Redis: connection timeout" (14:35:22)
   - "Session validation failed: session not found in store" (14:36:11)

**Timeline Analysis:**
- Session created → 2 min later → validation fails → user forced to re-auth
- Pattern repeats every ~2 minutes
- Coincides with Redis timeout error

### Step 4: Correlate Metrics + Logs = Root Cause
**Metrics show:** Redis response time 1250ms (should be <50ms), 8 timeouts  
**Logs show:** Session persistence failures, validation errors  
**Root Cause:** Redis connection pool exhaustion → sessions can't be stored/retrieved → validation fails → forced re-login

### Step 5: Document Resolution
Use the resolution form to document:

**Root Cause Analysis:**
```
Redis connection pool was exhausted due to high memory usage (89%) and slow 
connection times (1250ms avg). This caused session persistence failures, 
leading to "session not found" validation errors and forced re-authentication.
```

**Solution Implemented:**
```
1. Restarted Redis service to clear stale connections
2. Increased connection pool size from 50 to 100
3. Applied memory leak patch to session manager
4. Verified session validation returned to normal (<100ms)
```

**Prevention Strategy:**
```
- Add CloudWatch alerts for Redis connection pool utilization >80%
- Implement connection pool auto-scaling based on load
- Weekly review of Redis metrics and connection patterns
- Add circuit breaker for session service to fail gracefully
```

---

## Example 2: Diagnosing Dashboard Slowdown (ticket_002)

### Step 1: Review the Ticket
- **Symptoms:** Dashboard takes 8–15 seconds to load during morning peak (8:30–9:30am)
- **Severity:** Medium
- **Environment:** Staging, Chrome, Windows

### Step 2: Check Auto-Detected Issues
**Issues Flagged:**
- 🔴 **CRITICAL:** Database Pool - Connection pool nearly exhausted: 96% (threshold: 90%)
- 🟡 **HIGH:** Dashboard Service - Very slow response: 12400ms (threshold: 3000ms)
- 🟡 **HIGH:** Database Queries - Slow query performance: 4200ms avg (threshold: 1000ms)
- 🟡 **HIGH:** Server Resources - High disk I/O: 91% (threshold: 80%)

**Initial Hypothesis:** Database bottleneck causing slow dashboard rendering

### Step 3: Analyze Logs
Filter to **WARN** and **ERROR**:
- "Query took 8100ms, expected <500ms" on `department_aggregates` table
- "Connection pool exhausted: 50/50 connections active"
- Multiple slow query warnings (1150ms, 11200ms)

**Pattern:** Queries are consistently slow, pool is maxed out waiting for queries to complete

### Step 4: Root Cause Analysis
**Metrics:** 96% pool utilization, 4.2s avg query time, 91% disk I/O  
**Logs:** Specific table (`department_aggregates`) causing timeout  
**Root Cause:** Missing database index on frequently-queried column → full table scans → slow queries → pool exhaustion → dashboard timeout

### Step 5: Document Resolution
**Root Cause:**
```
Dashboard slowdown caused by missing index on department_aggregates table. 
Queries were performing full table scans (8+ seconds), exhausting the 
connection pool (96% utilized) and causing high disk I/O (91%).
```

**Solution:**
```
1. Added B-tree index on department_id column
2. Query time reduced from 8100ms to 200ms (97% improvement)
3. Connection pool utilization dropped to 45%
4. Dashboard load time now <2 seconds
```

**Prevention:**
```
- Regular query performance audits using EXPLAIN ANALYZE
- Automated index recommendations based on slow query logs
- Database connection pool monitoring with alerts at 80% utilization
- Load testing before deploying schema changes
```

---

## Best Practices for Using This Tool

### 1. Always Start with Metrics
The auto-detected issues provide a **starting point** for investigation. Use severity to prioritize:
- **CRITICAL:** Immediate action required (service down, data loss risk)
- **HIGH:** Significant user impact (performance degradation, errors)
- **MEDIUM:** Minor degradation (potential future issues)

### 2. Use Log Filtering Strategically
- Start with **ERROR** to find immediate failures
- Add **WARN** for early warning signs
- Use **INFO** to understand normal flow and context

### 3. Look for Patterns, Not Individual Events
- Repeated errors at intervals suggest resource exhaustion
- Errors followed by fallback warnings suggest graceful degradation
- Sudden spikes correlate with specific events (deploys, traffic patterns)

### 4. Correlate Across Data Sources
The best diagnoses come from connecting:
- **Metrics** (what is slow/failing)
- **Logs** (why it's failing)
- **Ticket symptoms** (user-reported impact)

### 5. Document Thoroughly
Good resolutions help the entire team:
- **Root cause:** Technical details for engineers
- **Solution:** Step-by-step for reproducibility
- **Prevention:** Process changes to avoid recurrence

### 6. Use Knowledge Base for Pattern Recognition
Before investigating, search KB for:
- Similar symptoms
- Same services/components
- Related error messages

This prevents duplicate troubleshooting effort.

---

## Interview Talking Points

**When discussing this project:**

> "I built a diagnostic tool that demonstrates the TSE methodology I use: 
> start with symptoms, check metrics for anomalies, dive into logs for 
> specifics, correlate data sources to identify root cause, then document 
> the resolution for future reference."

**Key phrases:**
- "Metric-driven diagnosis"
- "Log correlation and pattern recognition"
- "Automated issue detection using heuristics"
- "Building institutional knowledge through documentation"
- "Systematic troubleshooting methodology"