# Frontend Repair Status (App.jsx Tabs & Port Launch) – YYYY-MM-DD

## Overview
- Working repo: `GreenStack` (FastAPI backend + React frontend).
- Focus: fix JSX structure errors in `frontend/src/App.jsx`, ensure new port defaults (6173+) act correctly via `scripts/setup.bat`, and keep documentation aligned.
- This document captures the current state so another engineer can pick up without context loss.

## Completed Work
1. **Port/Setup Updates**
   - `scripts/setup.bat`, `src/config.py`, `src/start.py`: default dev server port now 6173 with automatic retry within the 6000–6999 range.
   - Docs refreshed (`README.md`, Windows install guide) to mention the new port behavior.

2. **JSX Audit Foundation**
   - Added `frontend/scripts/check-jsx.cjs` (uses `acorn-jsx`) to parse every `.jsx/.tsx` file for unmatched tags and missing closing fragments.
   - Ran initial audit; uncovered dozens of `TabsContent` sections returning multiple nodes.

3. **App.jsx Restructuring**
   - For each `<TabsContent>` (overview, parameters, images, errors, events, communication, menus, XML, technical, generate), the body now returns a single wrapper (`div` with `space-y-*` or similar). No raw `<>...</>` wrappers remain except in the `Sidebar` nav menu (intentional).
   - Extracted the entire Process Data view into a helper (`renderProcessDataTab`) so that:
     - The helper returns the monolithic markup.
     - The main JSX simply embeds `{renderProcessDataTab()}` inside `<TabsContent value="processdata">…`.
   - Port changes plus JSX adjustments touched `App.jsx`.

4. **Context Preservation**
   - Saved the *pre-refactor* Process Data markup under `/tmp/processdata_block.jsx` during the extraction; not needed anymore but noted here for reference.

## Current Blockers / Bugs
1. `npm run lint -- src/App.jsx` fails at `frontend/src/App.jsx:2558`:
   ```
   Parsing error: Adjacent JSX elements must be wrapped in an enclosing tag
   ```
   This happens because `renderProcessDataTab` currently returns a `<div>…</div>` sibling directly from the helper **and** the tab body wraps it inside `<TabsContent>`. Need to ensure there’s only one root element per tab.

2. `scripts\setup.bat` has not been re-run since the App.jsx edits; the user still sees Vite parser errors. Once lint passes, re-launch via the script to confirm the port logic works.

3. ESLint warnings remain for unused imports (`Alert`, `ScrollArea`, `Gauge`, etc.) in `App.jsx` and `components/AdminConsole.jsx`. They’re not fatal but should be cleaned once structural issues are gone.

4. The JSX audit script should be re-run once Process Data compiles:
   ```
   node frontend/scripts/check-jsx.cjs
   ```
   Currently it still flags the Process Data section.

## Next Steps (ordered)
1. **Fix Process Data Tab Root**
   - Update `renderProcessDataTab` to return just the inner markup (e.g., wrap everything in a fragment) and ensure `<TabsContent value="processdata">` has a single child.
   - Re-run `npm run lint -- src/App.jsx`.

2. **Run JSX Audit Script**
   - `node frontend/scripts/check-jsx.cjs`
   - If anything else errors, repeat the “single wrapper” cleanup for the reported file/line.

3. **Housekeep Warnings**
   - Remove unused imports in `App.jsx` and `components/AdminConsole.jsx`.
   - Re-run `npm run lint` to confirm all warnings are gone (unless intentionally suppressed).

4. **Full Launch Verification**
   - `scripts\setup.bat` (Windows) or `bash scripts/setup.bat` (WSL) to spin up backend + frontend.
   - Confirm Vite binds to 6173 or the next open port in 6000s.

5. **Git Hygiene**
   - Once satisfied, stage docs/port/App.jsx changes.
   - Prepare commit summarizing “App.jsx tab fixes + port behavior + doc cleanup”.

## Reference Files
- `frontend/src/App.jsx` — main problem area (see tabs around lines 2600–5100).
- `frontend/scripts/check-jsx.cjs` — structural audit script.
- `scripts/setup.bat`, `src/config.py`, `src/start.py` — port/launch logic.
- `README.md`, `docs/guides/...` — reflect new dev port guidance.

Feel free to ping if more context is needed; otherwise continue with “Next Steps” above. Replace “YYYY-MM-DD” in the title when updating.
