# Backend Restart Required

## Issue
The new PQA dashboard endpoints are returning 404 because the backend server hasn't loaded them yet.

## Solution: Restart Backend Server

### Windows (PowerShell)

```powershell
# Stop the backend (Ctrl+C in the terminal running it)
# Then restart:
cd F:\github\GreenStack
python -m uvicorn src.api:app --reload --host 0.0.0.0 --port 8000
```

### Alternative: Find and Kill Process

```powershell
# Find the process
netstat -ano | findstr :8000

# Kill it (replace PID with actual process ID)
taskkill /PID <PID> /F

# Start fresh
python -m uvicorn src.api:app --reload --host 0.0.0.0 --port 8000
```

### Linux/Mac

```bash
# Stop the backend (Ctrl+C)
# Then restart:
cd /path/to/GreenStack
python -m uvicorn src.api:app --reload --host 0.0.0.0 --port 8000
```

## Verify Endpoints Work

```bash
# Run the test script
python test_pqa_endpoints.py
```

Should show:
```
✓ OK     | /api/pqa/dashboard/summary
✓ OK     | /api/pqa/dashboard/score-distribution
✓ OK     | /api/pqa/dashboard/diff-distribution
✓ OK     | /api/pqa/dashboard/xpath-patterns?limit=10
✓ OK     | /api/pqa/dashboard/phase-breakdown
```

## Expected Behavior After Restart

1. Console logs will stop showing 404 errors
2. Console will show:
   ```
   [PQA Enhanced] Results: {
     scoreDistribution: true,
     diffDistribution: true,
     xpathPatterns: true,
     phaseBreakdown: true
   }
   ```
3. Dashboard will display:
   - Score distribution histogram
   - Diff type breakdown
   - XPath patterns (clickable)
   - Phase breakdown (5 phases)
   - Export buttons (JSON/CSV)

## Why This Happened

The new API endpoints were added to `src/routes/pqa_routes.py` but the backend server was still running with the old code. Python doesn't automatically reload route changes unless using `--reload` flag AND the files are monitored correctly.

## Auto-Reload Note

If using `--reload` flag, uvicorn should detect file changes. However, sometimes it misses updates in imported modules. Manual restart is most reliable.
