# Next Steps – 2025-11-20

## Current Status
- **Backend**: FastAPI server boots cleanly on port 8000 (health check confirmed).
- **Frontend**: Vite fails immediately because the optional Rollup native binary (`@rollup/rollup-win32-x64-msvc`) was not installed. This is the npm optional-deps bug mentioned in the stack trace and causes `npm run dev` inside `scripts/setup.bat` to exit.
- **Environment**: Redis is reachable but unauthenticated for rate limiting/caching (same warnings as before); otherwise services look normal.

## Blocking Issue
```
Error: Cannot find module @rollup/rollup-win32-x64-msvc.
npm currently has a bug with optional dependencies.
```
Until the Rollup binary is re-installed, the frontend cannot stay up and the overall `setup.bat` orchestration shuts everything down.

## Next Actions
1. **Clean npm install**
   - From `frontend/` remove `node_modules` and `package-lock.json`.
   - Reinstall dependencies via `npm install`.
2. **Rerun setup**
   - Execute `scripts\setup.bat` (or `bash scripts/setup.bat` under WSL) to relaunch backend + frontend.
   - Confirm Vite now binds to 6173 (or the next open port) with no missing-module errors.
3. **Smoke tests**
   - Load http://localhost:6173 and ensure the updated Process Data tab renders and exports still work.
   - Open Admin Console → Parser Diagnostics to confirm vendor charts and MQTT cards load correctly.
4. **If Rollup fails again**
   - Clear npm cache (`npm cache clean --force`) before reinstalling.
   - As a fallback, install the binary explicitly: `npm i @rollup/rollup-win32-x64-msvc`.

Please record the outcome (success/failure) back in this folder so the next engineer knows whether additional remediation is required.
