# Directory Structure Audit - GreenStack

**Date:** 2025-11-25
**Status:** In Progress
**Purpose:** Classify and document all top-level directories

---

## Summary

**Total Top-Level Directories:** 13

| Status | Count | Classification |
|--------|-------|----------------|
| ✓ Keep | 8 | Essential application directories |
| ⚠️ Review | 2 | May contain cruft or be empty |
| ❌ Remove | 3 | Should be gitignored (generated/storage) |

---

## Directory Inventory

### 1. Core Application Code ✓

#### `src/`
**Purpose:** Python backend source code
**Status:** ✓ Keep
**Contents:**
- API routes (FastAPI)
- Business logic services
- Data models
- Parsers (IODD/EDS/PQA)
- Storage management
- Utility modules

**Actions:**
- [ ] Audit for dead code
- [ ] Verify organization matches documented structure
- [ ] Check for TODO/FIXME comments

#### `frontend/`
**Purpose:** Astro/Starlight documentation platform
**Status:** ✓ Keep
**Contents:**
- `src/content/` - Documentation (Markdown/MDX)
- `src/components/` - Reusable components
- `src/layouts/` - Page layouts
- `node_modules/` - Dependencies (gitignored)
- `dist/` - Build output (gitignored)

**Actions:**
- [ ] Verify frontend/src/content is populated with docs
- [ ] Check for unused components
- [ ] Audit dependencies in package.json

#### `services/` (if present)
**Purpose:** TBD - may be microservices or service layer
**Status:** ⚠️ Review
**Contents:** TBD

**Actions:**
- [ ] Determine purpose
- [ ] Check if still in use
- [ ] Consolidate with src/ if redundant

---

### 2. Infrastructure & Configuration ✓

#### `alembic/`
**Purpose:** Database migrations (Alembic)
**Status:** ✓ Keep
**Contents:**
- `versions/` - Migration files
- `env.py` - Alembic environment

**Actions:**
- [ ] Review migration history for orphaned files
- [ ] Check for archive/ subdirectory
- [ ] Ensure migrations are sequential and clean

#### `config/`
**Purpose:** Configuration files
**Status:** ✓ Keep
**Contents:**
- `grafana-monitoring/` - Grafana dashboards and provisioning
- Other config files (TBD)

**Actions:**
- [ ] Verify no secrets in config files
- [ ] Document purpose of each config subdirectory
- [ ] Ensure configs use environment variables

#### `deployment/`
**Purpose:** Deployment scripts and configurations
**Status:** ✓ Keep
**Contents:** TBD

**Actions:**
- [ ] Review deployment scripts
- [ ] Ensure docs reference these scripts
- [ ] Update if outdated

#### `scripts/`
**Purpose:** Utility scripts
**Status:** ✓ Keep
**Contents:**
- `backup.bat`, `backup.sh` - Backup scripts
- `check-backup-age.sh` - Backup verification
- `generate-secrets.bat`, `generate-secrets.sh` - Secret generation
- `setup_debug.bat` - Debug setup (recently moved here)
- `test_*.bat` - Test utilities (recently moved here)

**Actions:**
- [ ] Document purpose of each script
- [ ] Remove obsolete scripts
- [ ] Ensure scripts are referenced in docs

---

### 3. Testing & Test Data ✓

#### `tests/`
**Purpose:** Test suite (pytest)
**Status:** ✓ Keep
**Contents:** Unit tests, integration tests

**Actions:**
- [ ] Verify tests are organized
- [ ] Check test coverage
- [ ] Remove obsolete tests
- [ ] Ensure tests run in CI

#### `test-data/`
**Purpose:** Sample IODD/EDS files and test fixtures
**Status:** ✓ Keep
**Contents:**
- `iodd/` or `iodd-files/` - Sample IODD files
- `eds/` or `eds-files/` - Sample EDS files
- `output/` - Test output (should be gitignored)
- Fixtures and sample data

**Size Note:** May contain thousands of zip files (6,738 per baseline)

**Actions:**
- [ ] Review if all test data is necessary
- [ ] Consider reducing number of test files
- [ ] Ensure temp directories are gitignored
- [ ] Document purpose of test data sets

---

### 4. Documentation ⚠️

#### `docs/`
**Purpose:** DEPRECATED - Legacy documentation
**Status:** ⚠️ TO BE MIGRATED/REMOVED
**Target:** Migrate all to `frontend/src/content/`

**Contents:**
- Architecture docs
- API reference
- Development guides
- Various reports and notes
- `archive/` subdirectory
- `audits/` subdirectory (audit outputs - KEEP)

**Actions:**
- [ ] Inventory all .md files
- [ ] Identify duplicates with frontend/src/content
- [ ] Migrate relevant content to frontend
- [ ] **KEEP docs/audits/** - audit baseline outputs
- [ ] Remove obsolete docs
- [ ] Delete empty docs/ after migration (or keep only audits/)

---

### 5. Generated/Storage Directories ❌

These should be GITIGNORED and not tracked:

#### `generated/`
**Purpose:** Generated files (temp output)
**Status:** ❌ Should be gitignored
**Actions:**
- [ ] Verify `.gitignore` includes `generated/`
- [ ] Remove from repository if tracked
- [ ] Check if directory is needed or can be deleted

#### `iodd_storage/`
**Purpose:** Uploaded/processed IODD files
**Status:** ❌ Should be gitignored (already is)
**Actions:**
- [ ] Confirm gitignored
- [ ] Document purpose in platform docs
- [ ] Configure storage path via environment variable

#### `ticket_attachments/`
**Purpose:** Ticket/issue attachments
**Status:** ❌ Should be gitignored (already is)
**Actions:**
- [ ] Confirm gitignored
- [ ] Document purpose
- [ ] Configure path via environment variable

---

## Ideal Directory Structure

After cleanup and migration:

```
GreenStack/
├── .github/              # CI/CD workflows
├── alembic/              # Database migrations
│   ├── versions/         # Migration files (clean, sequential)
│   └── env.py
├── config/               # Configuration files (no secrets)
│   └── grafana-monitoring/
├── deployment/           # Deployment scripts and configs
├── docs/                 # ONLY audit outputs remain
│   └── audits/
│       ├── templates/
│       └── audit-baseline/
├── frontend/             # Documentation platform
│   ├── node_modules/     # (gitignored)
│   ├── dist/             # (gitignored)
│   ├── src/
│   │   ├── content/      # ALL DOCUMENTATION HERE
│   │   ├── components/
│   │   └── layouts/
│   └── package.json
├── generated/            # (gitignored - runtime generated files)
├── iodd_storage/         # (gitignored - uploaded files)
├── scripts/              # Utility scripts (documented)
├── src/                  # Python backend
│   ├── api/
│   ├── models/
│   ├── parsers/
│   ├── services/
│   ├── storage/
│   └── main.py
├── test-data/            # Sample/fixture data (minimal, documented)
│   ├── iodd-files/
│   ├── eds-files/
│   └── README.md
├── tests/                # Test suite
├── ticket_attachments/   # (gitignored - runtime attachments)
└── [standard root files]
```

**Total: ~13-14 directories (plus gitignored runtime dirs)**

---

## Directory Classification

### Essential - Keep (8 directories)
1. `.github/` - CI/CD
2. `alembic/` - Database migrations
3. `config/` - Configuration
4. `deployment/` - Deployment
5. `frontend/` - Documentation platform
6. `scripts/` - Utilities
7. `src/` - Backend code
8. `tests/` - Test suite

### Review - May Need Cleanup (2 directories)
9. `test-data/` - Review size, document purpose
10. `services/` - Determine if needed or consolidate

### Generated/Storage - Should be Gitignored (3 directories)
11. `generated/` - Runtime generated files
12. `iodd_storage/` - Uploaded files
13. `ticket_attachments/` - Attachments

### Special Case - Partial Keep (1 directory)
14. `docs/` - Migrate contents to frontend, KEEP docs/audits/ only

---

## Size Analysis

**Large Directories to Review:**
- `test-data/` - Likely contains 6,738 zip files (from baseline stats)
  - Consider if all are necessary
  - May significantly impact repo size
- `frontend/node_modules/` - Should be gitignored ✓
- `iodd_storage/`, `ticket_attachments/`, `generated/` - Should be gitignored ✓

---

## Next Steps

### Immediate Actions
1. [ ] Check if `generated/`, `iodd_storage/`, `ticket_attachments/` are gitignored
2. [ ] Review `services/` directory purpose
3. [ ] Audit `test-data/` for necessity
4. [ ] Begin `docs/` migration to `frontend/src/content/`

### Documentation Actions
5. [ ] Document each directory's purpose in `frontend/src/content/docs/architecture/repository-layout.md`
6. [ ] Create README.md in key directories explaining their purpose
7. [ ] Update main README.md with directory overview

### Cleanup Actions
8. [ ] Remove `services/` if redundant
9. [ ] Reduce `test-data/` size if possible
10. [ ] After docs migration, remove legacy `docs/` (except `docs/audits/`)

---

**Status:** Section 2.2 - Audit Complete, Actions Pending
