# GitHub Issues to Create - From TODO Cleanup

**Date:** 2025-11-26
**Status:** Ready for Issue Creation
**Source:** Section 5.2 - Comment & Internal Notes Scrub

---

## Overview

The following GitHub issues should be created to track the functionality currently marked with TODO comments in the codebase. After creating these issues, the TODO comments will be removed from the source code.

**Total Issues:** 5
**Priority Breakdown:**
- High: 0
- Medium: 5
- Low: 0

---

## Issue #1: DLQ Database Persistence

**Title:** Implement DLQ database persistence

**Labels:** `enhancement`, `backend`, `monitoring`, `dead-letter-queue`

**Priority:** Medium

**File:** `src/tasks/dlq_handler.py:66`

**Current Code:**
```python
# TODO: Store in database for analysis
```

**Description:**
Currently, dead letter queue messages are processed but not persisted to the database for analysis. This makes it difficult to track recurring failures and analyze patterns in task failures.

**Acceptance Criteria:**
- [ ] Create database table for DLQ message storage
- [ ] Store failed task details: task_id, task_name, args, kwargs, error message, stacktrace
- [ ] Include timestamp, retry count, and final status
- [ ] Provide admin API endpoint to query DLQ history
- [ ] Add database migration for new table
- [ ] Include retention policy (configurable days to keep DLQ records)

**Technical Notes:**
- Table name: `dlq_messages`
- Should integrate with existing SQLite/PostgreSQL setup
- Consider indexing on task_name and timestamp for query performance

**Related Files:**
- `src/tasks/dlq_handler.py` - Implementation location
- `alembic/versions/` - Database migration needed

---

## Issue #2: DLQ Alert/Notification System

**Title:** Implement DLQ alert/notification system

**Labels:** `enhancement`, `backend`, `monitoring`, `notifications`

**Priority:** Medium

**File:** `src/tasks/dlq_handler.py:67`

**Current Code:**
```python
# TODO: Send alert/notification (email, Slack, PagerDuty, etc.)
```

**Description:**
Dead letter queue should send alerts when tasks fail repeatedly to notify administrators of issues requiring attention.

**Acceptance Criteria:**
- [ ] Email notifications for critical failures
- [ ] Slack integration (optional, configurable)
- [ ] PagerDuty integration (optional, configurable)
- [ ] Configurable alert thresholds (e.g., alert after N failures in M minutes)
- [ ] Alert rate limiting to prevent notification spam
- [ ] Template system for notification messages
- [ ] Admin UI to configure notification settings

**Technical Notes:**
- Use environment variables for SMTP/Slack/PagerDuty credentials
- Consider using Celery beat for threshold checking
- Alert templates should include: task name, error type, failure count, timestamp

**Dependencies:**
- Requires Issue #1 (DLQ Database Persistence) for failure counting

**Configuration Example:**
```env
DLQ_ALERT_EMAIL=admin@example.com
DLQ_ALERT_THRESHOLD=5
DLQ_ALERT_WINDOW_MINUTES=15
DLQ_SLACK_WEBHOOK_URL=https://...
```

**Related Files:**
- `src/tasks/dlq_handler.py` - Implementation location
- `src/config.py` - Configuration settings
- `templates/emails/` - Email templates

---

## Issue #3: DLQ Automatic Recovery

**Title:** Implement DLQ automatic recovery mechanism

**Labels:** `enhancement`, `backend`, `monitoring`, `resilience`

**Priority:** Low to Medium

**File:** `src/tasks/dlq_handler.py:68`

**Current Code:**
```python
# TODO: Attempt recovery if applicable
```

**Description:**
Some failed tasks could be automatically recovered based on the error type and context. This would reduce manual intervention for transient failures.

**Acceptance Criteria:**
- [ ] Identify recoverable error types (network timeout, database connection, etc.)
- [ ] Implement automatic retry with exponential backoff
- [ ] Configure max retry attempts per task
- [ ] Track retry history in database
- [ ] Support for retry delay strategies (fixed, exponential, jittered)
- [ ] Admin override to disable auto-recovery for specific tasks

**Recovery Strategy:**
```python
RECOVERABLE_ERRORS = [
    'ConnectionError',
    'TimeoutError',
    'DatabaseConnectionError',
    'TemporaryNetworkIssue'
]

RETRY_DELAYS = [60, 300, 900, 3600]  # 1min, 5min, 15min, 1hour
MAX_AUTO_RETRIES = 4
```

**Technical Notes:**
- Check error type/message to determine if recoverable
- Use Celery's built-in retry mechanism where possible
- Log all retry attempts for auditing

**Dependencies:**
- Requires Issue #1 (DLQ Database Persistence) for retry tracking

**Related Files:**
- `src/tasks/dlq_handler.py` - Implementation location
- `src/config.py` - Recovery configuration

---

## Issue #4: DLQ Statistics Database Query

**Title:** Implement DLQ statistics database query

**Labels:** `bug`, `backend`, `monitoring`

**Priority:** Medium

**File:** `src/tasks/dlq_handler.py:134`

**Current Code:**
```python
def get_dlq_stats(self) -> Dict[str, Any]:
    """
    Get statistics about failed tasks in the Dead Letter Queue.

    Returns:
        dict: DLQ statistics
    """
    # TODO: Query database for DLQ statistics
    # For now, return placeholder data

    return {
        "total_failed_tasks": 0,
        "failed_today": 0,
        # ... placeholder data ...
    }
```

**Description:**
The `get_dlq_stats()` function currently returns placeholder data. It should query the actual DLQ database to provide meaningful statistics.

**Acceptance Criteria:**
- [ ] Query total failed tasks from database
- [ ] Calculate failed tasks by time period (today, this week, this month)
- [ ] Group failures by task type
- [ ] Calculate error type distribution
- [ ] Include average time to recovery (if auto-recovery enabled)
- [ ] Provide trend data (increasing/decreasing failure rates)

**Statistics to Return:**
```python
{
    "total_failed_tasks": int,
    "failed_today": int,
    "failed_this_week": int,
    "failed_this_month": int,
    "by_task_type": {
        "task_name": count,
        ...
    },
    "by_error_type": {
        "error_type": count,
        ...
    },
    "avg_recovery_time_seconds": float,
    "recovery_success_rate": float,
    "trend": "increasing" | "decreasing" | "stable"
}
```

**Dependencies:**
- Requires Issue #1 (DLQ Database Persistence)

**Related Files:**
- `src/tasks/dlq_handler.py` - Implementation location
- `src/routes/admin_routes.py` - API endpoint integration

---

## Issue #5: Track PQA Reconstruction Performance Metrics

**Title:** Track PQA reconstruction and comparison times

**Labels:** `enhancement`, `backend`, `monitoring`, `pqa`

**Priority:** Medium

**File:** `src/utils/pqa_orchestrator.py:290`

**Current Code:**
```python
passed, not passed, 0, 0  # TODO: Track actual times
```

**Description:**
PQA quality metrics should track actual reconstruction and comparison times for performance monitoring and optimization.

**Acceptance Criteria:**
- [ ] Measure reconstruction time accurately (start to end)
- [ ] Measure comparison time accurately (diff analysis duration)
- [ ] Store times in `pqa_quality_metrics` table
- [ ] Provide performance trending in admin dashboard
- [ ] Add alerts for slow reconstructions (> threshold)
- [ ] Track performance by file size/complexity

**Implementation Approach:**
```python
import time

# Before reconstruction
start_reconstruct = time.time()
reconstructed = self._reconstruct_file(file_id, file_type)
reconstruction_time_ms = int((time.time() - start_reconstruct) * 1000)

# Before comparison
start_compare = time.time()
metrics, diff_items = self._analyze_diff(original, reconstructed, file_type)
comparison_time_ms = int((time.time() - start_compare) * 1000)

# Store actual times instead of 0, 0
cursor.execute("""
    INSERT INTO pqa_quality_metrics (
        ...,
        reconstruction_time_ms,
        comparison_time_ms
    ) VALUES (?, ?, ..., ?, ?)
""", (..., reconstruction_time_ms, comparison_time_ms))
```

**Performance Thresholds:**
- Warning: reconstruction > 5000ms (5 seconds)
- Critical: reconstruction > 30000ms (30 seconds)
- Warning: comparison > 2000ms (2 seconds)

**Admin Dashboard Features:**
- [ ] Average reconstruction time by file type (IODD vs EDS)
- [ ] Slowest reconstructions (top 10)
- [ ] Performance trend over time (chart)
- [ ] Performance by file size correlation

**Related Files:**
- `src/utils/pqa_orchestrator.py` - Implementation location
- `src/routes/admin_routes.py` - Dashboard integration
- `frontend/src/components/pqa/` - Dashboard UI

---

## Issue Creation Checklist

When creating these issues on GitHub:

- [ ] Copy title and description from above
- [ ] Add appropriate labels
- [ ] Set priority/milestone if applicable
- [ ] Link related issues (e.g., dependencies)
- [ ] Add to project board if using one
- [ ] Assign to team member if known

---

## After Issue Creation

Once all issues are created on GitHub:

1. [ ] Remove TODO comments from source files:
   - `src/tasks/dlq_handler.py` (lines 66-68, 134)
   - `src/utils/pqa_orchestrator.py` (line 290)

2. [ ] Update this document with issue numbers:
   - Issue #1: DLQ Database Persistence → GitHub Issue #XXX
   - Issue #2: DLQ Alert/Notification → GitHub Issue #XXX
   - Issue #3: DLQ Automatic Recovery → GitHub Issue #XXX
   - Issue #4: DLQ Statistics Query → GitHub Issue #XXX
   - Issue #5: Track PQA Performance → GitHub Issue #XXX

3. [ ] Commit changes:
   ```bash
   git add src/tasks/dlq_handler.py src/utils/pqa_orchestrator.py
   git commit -m "chore: remove TODO comments, tracked in GitHub issues"
   ```

---

## Summary

**Total Development Effort Estimate:**
- Issue #1 (DLQ Persistence): 4-6 hours
- Issue #2 (DLQ Alerts): 6-8 hours
- Issue #3 (DLQ Recovery): 4-6 hours
- Issue #4 (DLQ Statistics): 2-3 hours
- Issue #5 (PQA Performance): 2-3 hours

**Total: 18-26 hours**

**Recommended Implementation Order:**
1. Issue #1 (DLQ Persistence) - Foundation for other features
2. Issue #4 (DLQ Statistics) - Depends on #1, provides visibility
3. Issue #5 (PQA Performance) - Independent, quick win
4. Issue #2 (DLQ Alerts) - Depends on #1, high value
5. Issue #3 (DLQ Recovery) - Depends on #1, lower priority

---

**Status:** Ready for GitHub Issue Creation
**Next Step:** Create issues on GitHub, then remove TODO comments from source
