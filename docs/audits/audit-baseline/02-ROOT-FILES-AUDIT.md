# Root Files Audit - GreenStack

**Date:** 2025-11-25
**Status:** In Progress
**Purpose:** Categorize all root-level files and determine keep/remove/relocate

---

## Summary

**Total Root Files Found:** 44
- **Keep (Standard):** 7
- **Keep (Project-specific):** 8
- **Remove (Debug/Test scripts):** 21
- **Remove (Generated/Temp):** 4
- **Relocate:** 4

---

## 1. Standard Files - KEEP ✓

These are standard repository files that should remain in root:

| File | Status | Notes |
|------|--------|-------|
| `README.md` | ✓ Keep | Project overview - needs review for accuracy |
| `LICENSE.md` | ✓ Keep | Legal license |
| `.gitignore` | ✓ Keep | Comprehensive, may need updates |
| `.dockerignore` | ✓ Keep | Docker build optimization |
| `.pre-commit-config.yaml` | ✓ Keep | Pre-commit hooks configuration |
| - | ❌ Missing | **CONTRIBUTING.md** - needs to be created |
| - | ❌ Missing | **CODE_OF_CONDUCT.md** - needs to be created |
| - | ❌ Missing | **SECURITY.md** - needs to be created |
| - | ❌ Missing | **CHANGELOG.md** - needs to be created |

**Actions:**
- [ ] Review and update `README.md`
- [ ] Create `CONTRIBUTING.md`
- [ ] Create `CODE_OF_CONDUCT.md`
- [ ] Create `SECURITY.md`
- [ ] Create `CHANGELOG.md`

---

## 2. Project Configuration Files - KEEP ✓

Essential configuration files for the project:

| File | Status | Purpose |
|------|--------|---------|
| `pyproject.toml` | ✓ Keep | Python project configuration |
| `requirements.txt` | ✓ Keep | Python dependencies |
| `pytest.ini` | ✓ Keep | Pytest configuration |
| `.pylintrc` | ✓ Keep | Pylint configuration (or migrate to pyproject.toml) |
| `alembic.ini` | ✓ Keep | Database migration config |
| `MANIFEST.in` | ✓ Keep | Python package manifest |
| `Dockerfile` | ✓ Keep | Container configuration |
| `mkdocs.yml` | ⚠️ Review | MkDocs config - may be obsolete if using Astro/Starlight |

**Actions:**
- [ ] Review if `mkdocs.yml` is still needed (likely obsolete)
- [ ] Consider consolidating `.pylintrc` into `pyproject.toml`

---

## 3. Docker Compose Files - KEEP ✓

Multiple docker-compose files for different purposes:

| File | Status | Purpose |
|------|--------|---------|
| `docker-compose.yml` | ✓ Keep | Main docker composition |
| `docker-compose.iot.yml` | ✓ Keep | IoT-specific services |
| `docker-compose.monitoring.yml` | ✓ Keep | Grafana/Prometheus monitoring |
| `docker-compose.observability.yml` | ✓ Keep | Observability stack |
| `docker-compose.postgres.yml` | ✓ Keep | PostgreSQL database |

**Actions:**
- [ ] Document purpose of each compose file in README or docs
- [ ] Consider consolidating if some are redundant

---

## 4. Environment Templates - KEEP ✓

Environment configuration templates:

| File | Status | Purpose |
|------|--------|---------|
| `.env.example` | ✓ Keep | General environment template |
| `.env.iot.example` | ✓ Keep | IoT-specific environment |
| `.env.production.template` | ✓ Keep | Production environment template |

**Actions:**
- [ ] Ensure no real secrets in templates
- [ ] Verify all required variables are documented

---

## 5. DEBUG/TEST SCRIPTS - REMOVE ❌

**These should be deleted or moved to a separate testing/debug directory:**

### Debug Scripts (10 files)
- `code_quality_analyzer.py` - One-off analysis script
- `debug_metric_22.py` - Specific debug script
- `debug_reconstruction.py` - Debug script
- `diagnose_structural_issues.py` - Diagnostic script
- `diagnose_text_id_issue.py` - Diagnostic script
- `extract_tabs.py` - Data extraction script
- `reprocess_eds_files.py` - Reprocessing script
- `rerun_device56_analysis.py` - Specific analysis
- `reupload_device_27_complete.py` - Specific upload script
- `update_features_comparison.py` - Feature comparison script

### Test Scripts (11 files)
- `test_all_eds_pqa.py` - EDS/PQA testing
- `test_captron_import.py` - Import testing
- `test_current_reconstruction.py` - Reconstruction test
- `test_delete_all.py` - Deletion test
- `test_enum_pqa_device_27.py` - Device-specific test
- `test_error_event_collections.py` - Error/event test
- `test_iodd_imports.py` - IODD import test
- `test_menu_reconstruction.py` - Menu reconstruction test
- `test_pqa_analyzer.py` - PQA analyzer test
- `test_pqa_ticket_generation.py` - Ticket generation test
- `test_processdata_fix.py` - Process data fix test
- `test_ticket_creation_debug.py` - Ticket creation debug
- `test_ticket_generation.py` - Ticket generation test

**Total: 21 debug/test scripts**

**Actions:**
- [ ] Review each script to determine if any logic should be preserved
- [ ] Move useful test scripts to `tests/` directory with proper pytest structure
- [ ] Delete ad-hoc debug scripts
- [ ] Delete device-specific one-off scripts

---

## 6. BATCH FILES - RELOCATE TO `scripts/` 📁

These should be in the `scripts/` directory:

- `setup_debug.bat` - Debug setup script
- `test_pause.bat` - Test pause utility
- `test_setup_cleanup.bat` - Test cleanup utility
- `test_startup.bat` - Test startup script

**Actions:**
- [ ] Move to `scripts/` directory
- [ ] Ensure they're documented
- [ ] Consider if they're still needed

---

## 7. GENERATED/TEMP FILES - REMOVE ❌

These are generated output files that should not be in the repository:

- `codebase_stats.json` - Generated statistics
- `reprocess_output.txt` - Processing output log
- `test_output.txt` - Test output log
- `test-tickets.csv` - Test data output

**Actions:**
- [ ] Delete from repository
- [ ] Add patterns to `.gitignore`:
  - `*_output.txt`
  - `*.csv` (or specific patterns)
  - `codebase_stats.json`

---

## 8. DATABASE FILE - SHOULD BE GITIGNORED

- `greenstack.db` - SQLite database (2.7GB!)

**Actions:**
- [ ] Verify `*.db` is in `.gitignore`
- [ ] This file should never have been committed
- [ ] Confirm it's already ignored in current `.gitignore`

---

## Cleanup Summary

### Files to Keep in Root (15)
- Standard files: README, LICENSE, .gitignore, etc.
- Config files: pyproject.toml, requirements.txt, pytest.ini, etc.
- Docker files: Dockerfile, docker-compose.*.yml
- Environment templates: .env.example, .env.iot.example, etc.

### Files to Create (5)
- CONTRIBUTING.md
- CODE_OF_CONDUCT.md
- SECURITY.md
- CHANGELOG.md
- ARCHITECTURE.md (optional, or link to frontend docs)

### Files to Remove (25)
- 21 debug/test scripts
- 4 generated/output files

### Files to Relocate (4)
- 4 batch files → `scripts/`

### Files to Review (1)
- mkdocs.yml - likely obsolete

---

## Ideal Root Directory State

After cleanup, root should contain approximately:

```
GreenStack/
├── .dockerignore
├── .env.example
├── .env.iot.example
├── .env.production.template
├── .github/
├── .gitignore
├── .pre-commit-config.yaml
├── .pylintrc (or remove if using pyproject.toml)
├── alembic/
├── alembic.ini
├── backend/ or src/
├── CHANGELOG.md (create)
├── CODE_OF_CONDUCT.md (create)
├── config/
├── CONTRIBUTING.md (create)
├── deployment/
├── docker-compose.iot.yml
├── docker-compose.monitoring.yml
├── docker-compose.observability.yml
├── docker-compose.postgres.yml
├── docker-compose.yml
├── docs/ (to be migrated/removed)
├── Dockerfile
├── frontend/
├── LICENSE.md
├── MANIFEST.in
├── mkdocs.yml (review/remove)
├── pyproject.toml
├── pytest.ini
├── README.md
├── requirements.txt
├── scripts/
├── SECURITY.md (create)
└── test-data/
```

**Total: ~25 files + directories (down from 44+ files)**

---

## Next Steps

1. [ ] Create missing standard files (CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, CHANGELOG)
2. [ ] Review debug/test scripts for any logic to preserve
3. [ ] Delete obsolete debug/test scripts (21 files)
4. [ ] Delete generated/temp files (4 files)
5. [ ] Relocate batch files to scripts/ (4 files)
6. [ ] Review and possibly remove mkdocs.yml
7. [ ] Update .gitignore to prevent re-addition
8. [ ] Verify greenstack.db is properly ignored
9. [ ] Update README.md to reflect clean state

**Status:** Section 2.1 - Audit Complete, Actions Pending
