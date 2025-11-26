# Documentation Inventory & Migration Plan

**Date:** 2025-11-25
**Status:** In Progress
**Total Markdown Files:** 33

---

## Summary

| Location | Count | Action |
|----------|-------|--------|
| Root (standard) | 2 | ✓ Keep in place |
| Component READMEs | 4 | ✓ Keep in place |
| Audit outputs | 5 | ✓ Keep (docs/audits/) |
| docs/guides/ | 7 | → Migrate to frontend |
| docs/references/ | 6 | → Migrate to frontend |
| docs/ (root level) | 4 | → Migrate to frontend |
| docs/reports/ | 1 | → Review/consolidate |
| **Total to migrate** | **18** | **To frontend/src/content/** |

---

## 1. Root-Level Files - KEEP IN PLACE ✓

Standard repository files that should remain in root:

| File | Purpose | Status |
|------|---------|--------|
| `./README.md` | Project overview and getting started | ✓ Keep, review content |
| `./LICENSE.md` | Legal license | ✓ Keep as-is |

**Actions:**
- [ ] Review README.md for accuracy
- [ ] Ensure README links to frontend docs
- [ ] No migration needed

---

## 2. Component READMEs - KEEP IN PLACE ✓

Local READMEs within specific directories:

| File | Purpose | Status |
|------|---------|--------|
| `./alembic/README.md` | Alembic migrations info | ✓ Keep |
| `./alembic/versions/archive/README.md` | Archive explanation | ✓ Keep |
| `./deployment/nginx/README.md` | Nginx config notes | ✓ Keep |
| `./frontend/README.md` | Frontend dev notes | ✓ Keep |
| `./tests/README.md` | Test suite info | ✓ Keep |

**Actions:**
- [ ] Review each for accuracy
- [ ] Ensure they complement (not duplicate) frontend docs
- [ ] No migration needed

---

## 3. Audit Outputs - KEEP IN docs/audits/ ✓

Current audit documentation (DO NOT migrate or delete):

| File | Purpose |
|------|---------|
| `./docs/audits/audit-baseline/00-OBJECTIVES.md` | Audit objectives |
| `./docs/audits/audit-baseline/01-PLATFORM-CONVENTIONS.md` | Platform standards |
| `./docs/audits/audit-baseline/02-ROOT-FILES-AUDIT.md` | Root cleanup audit |
| `./docs/audits/audit-baseline/03-DIRECTORY-STRUCTURE-AUDIT.md` | Directory audit |
| `./docs/audits/audit-baseline/TASK_LIST.md` | Master task list |
| `./docs/audits/templates/repo-audit-cleanup-plan.md` | Audit template |

**Actions:**
- [ ] Keep all audit outputs in docs/audits/
- [ ] This is the ONLY content to remain in docs/

---

## 4. Documentation to Migrate - docs/guides/ (7 files)

### Accessibility
**File:** `./docs/guides/ACCESSIBILITY.md`
**Target:** `frontend/src/content/docs/development/accessibility.md`
**Category:** Development standards
**Priority:** Medium

### Contributing
**File:** `./docs/guides/CONTRIBUTING.md`
**Target:** Move to root as `./CONTRIBUTING.md` (standard location)
**Category:** Repository standard file
**Priority:** High
**Notes:** This should be a root file, not in docs/

### Developer Guide
**File:** `./docs/guides/DEVELOPER_GUIDE.md`
**Target:** `frontend/src/content/docs/development/developer-guide.md`
**Category:** Development guide
**Priority:** High
**Notes:** Core dev documentation

### Deployment Runbook
**File:** `./docs/guides/operations/DEPLOYMENT_RUNBOOK.md`
**Target:** `frontend/src/content/docs/deployment/runbook.md`
**Category:** Operations
**Priority:** High

### Disaster Recovery
**File:** `./docs/guides/operations/DISASTER_RECOVERY.md`
**Target:** `frontend/src/content/docs/operations/disaster-recovery.md`
**Category:** Operations
**Priority:** Medium

### Monitoring Setup Guide
**File:** `./docs/guides/operations/MONITORING_SETUP_GUIDE.md`
**Target:** `frontend/src/content/docs/operations/monitoring-setup.md`
**Category:** Operations
**Priority:** Medium
**Notes:** May overlap with existing monitoring docs

### Scaling Guide
**File:** `./docs/guides/operations/SCALING_GUIDE.md`
**Target:** `frontend/src/content/docs/operations/scaling.md`
**Category:** Operations
**Priority:** Low

### Troubleshooting
**File:** `./docs/guides/TROUBLESHOOTING.md`
**Target:** `frontend/src/content/docs/troubleshooting/guide.md`
**Category:** User/dev support
**Priority:** High

---

## 5. Documentation to Migrate - docs/references/ (6 files)

### API Documentation
**File:** `./docs/references/api/API_DOCUMENTATION.md`
**Target:** `frontend/src/content/docs/api/documentation.md` or consolidate with API_REFERENCE
**Category:** API reference
**Priority:** High
**Notes:** May be duplicate of API_REFERENCE.md

### API Reference
**File:** `./docs/references/api/API_REFERENCE.md`
**Target:** `frontend/src/content/docs/api/reference.md`
**Category:** API reference
**Priority:** High
**Notes:** Consolidate with API_DOCUMENTATION if duplicate

### Architecture
**File:** `./docs/references/ARCHITECTURE.md`
**Target:** `frontend/src/content/docs/architecture/overview.md`
**Category:** Architecture
**Priority:** High
**Notes:** Core documentation

### Components Inventory
**File:** `./docs/references/COMPONENTS_INVENTORY.md`
**Target:** `frontend/src/content/docs/architecture/components.md`
**Category:** Architecture
**Priority:** Medium

### Database Schema
**File:** `./docs/references/DATABASE_SCHEMA.md`
**Target:** `frontend/src/content/docs/database/schema.md`
**Category:** Database
**Priority:** High

### PQA Architecture
**File:** `./docs/references/PQA_ARCHITECTURE.md`
**Target:** `frontend/src/content/docs/features/pqa/architecture.md`
**Category:** Feature documentation
**Priority:** High
**Notes:** Core PQA documentation

---

## 6. Documentation to Migrate - docs/ Root Level (4 files)

### Markdown Inventory
**File:** `./docs/markdown_inventory.md`
**Action:** DELETE (obsolete - replaced by this audit)
**Priority:** N/A
**Notes:** Old inventory, no longer needed

### PQA Developer Guide
**File:** `./docs/PQA_DEVELOPER_GUIDE.md`
**Target:** `frontend/src/content/docs/features/pqa/developer-guide.md`
**Category:** Feature documentation
**Priority:** High

### PQA EDS IODD Separation
**File:** `./docs/PQA_EDS_IODD_SEPARATION.md`
**Target:** `frontend/src/content/docs/features/pqa/eds-iodd-separation.md`
**Category:** Feature documentation
**Priority:** Medium

### PQA System Overview
**File:** `./docs/PQA_SYSTEM_OVERVIEW.md`
**Target:** `frontend/src/content/docs/features/pqa/overview.md`
**Category:** Feature documentation
**Priority:** High

### README
**File:** `./docs/README.md`
**Action:** DELETE or consolidate into frontend docs index
**Priority:** Low
**Notes:** Likely duplicates project README

---

## 7. Reports - docs/reports/ (1 file)

### Changelog
**File:** `./docs/reports/CHANGELOG.md`
**Target:** `./CHANGELOG.md` (move to root - standard location)
**Category:** Repository standard file
**Priority:** Medium
**Notes:** CHANGELOG should be a root file

---

## Migration Strategy

### Phase 1: Move Standard Files to Root
- [ ] Move `docs/guides/CONTRIBUTING.md` → `./CONTRIBUTING.md`
- [ ] Move `docs/reports/CHANGELOG.md` → `./CHANGELOG.md`
- [ ] Delete `docs/markdown_inventory.md` (obsolete)
- [ ] Delete `docs/README.md` (redundant)

### Phase 2: Create Frontend Doc Structure
Create these directories in `frontend/src/content/`:
- [ ] `docs/development/`
- [ ] `docs/deployment/`
- [ ] `docs/operations/`
- [ ] `docs/api/`
- [ ] `docs/architecture/`
- [ ] `docs/database/`
- [ ] `docs/features/pqa/`
- [ ] `docs/troubleshooting/`

### Phase 3: Migrate High Priority Docs (8 files)
1. [ ] ARCHITECTURE.md → frontend
2. [ ] DEVELOPER_GUIDE.md → frontend
3. [ ] API_REFERENCE.md + API_DOCUMENTATION.md → frontend (consolidate)
4. [ ] DATABASE_SCHEMA.md → frontend
5. [ ] PQA_ARCHITECTURE.md → frontend
6. [ ] PQA_DEVELOPER_GUIDE.md → frontend
7. [ ] PQA_SYSTEM_OVERVIEW.md → frontend
8. [ ] DEPLOYMENT_RUNBOOK.md → frontend
9. [ ] TROUBLESHOOTING.md → frontend

### Phase 4: Migrate Medium Priority Docs (5 files)
1. [ ] COMPONENTS_INVENTORY.md → frontend
2. [ ] DISASTER_RECOVERY.md → frontend
3. [ ] MONITORING_SETUP_GUIDE.md → frontend
4. [ ] ACCESSIBILITY.md → frontend
5. [ ] PQA_EDS_IODD_SEPARATION.md → frontend

### Phase 5: Migrate Low Priority Docs (1 file)
1. [ ] SCALING_GUIDE.md → frontend

### Phase 6: Cleanup
- [ ] Verify all migrations complete
- [ ] Delete empty docs/ subdirectories
- [ ] Keep only docs/audits/ in docs/
- [ ] Update all internal links

---

## Deduplication Analysis

### Potential Duplicates to Review:
1. **API Documentation:**
   - `API_DOCUMENTATION.md` vs `API_REFERENCE.md`
   - **Action:** Review both, consolidate into single comprehensive API reference

2. **README files:**
   - `./README.md` (root)
   - `docs/README.md`
   - **Action:** Keep root README, delete docs/README if redundant

3. **Monitoring:**
   - `MONITORING_SETUP_GUIDE.md`
   - May overlap with existing frontend monitoring docs
   - **Action:** Review frontend docs, consolidate if duplicate

4. **PQA Documentation:**
   - Multiple PQA docs (overview, architecture, developer guide, separation)
   - **Action:** Organize as coherent section in frontend under `features/pqa/`

---

## File Migration Checklist Template

For each file to migrate:
- [ ] Read original file
- [ ] Identify target location in frontend
- [ ] Check for duplicates in frontend
- [ ] Convert to Starlight format (add frontmatter)
- [ ] Update internal links
- [ ] Update code references
- [ ] Add to sidebar navigation
- [ ] Test rendering in dev server
- [ ] Delete original after verification

---

## Expected Frontend Documentation Structure

After migration:

```
frontend/src/content/docs/
├── index.md (Project overview)
├── development/
│   ├── developer-guide.md
│   └── accessibility.md
├── deployment/
│   └── runbook.md
├── operations/
│   ├── disaster-recovery.md
│   ├── monitoring-setup.md
│   └── scaling.md
├── api/
│   └── reference.md (consolidated)
├── architecture/
│   ├── overview.md
│   └── components.md
├── database/
│   └── schema.md
├── features/
│   └── pqa/
│       ├── overview.md
│       ├── architecture.md
│       ├── developer-guide.md
│       └── eds-iodd-separation.md
└── troubleshooting/
    └── guide.md
```

---

## Quality Assurance

After migration, verify:
- [ ] All internal links work
- [ ] Code examples are accurate
- [ ] Diagrams render correctly
- [ ] Sidebar navigation is logical
- [ ] Search finds key terms
- [ ] No broken image links
- [ ] Frontmatter is correct
- [ ] No duplicate content

---

## Timeline Estimate

- **Phase 1 (Standard files):** 1 hour
- **Phase 2 (Frontend structure):** 30 minutes
- **Phase 3 (High priority):** 4-6 hours
- **Phase 4 (Medium priority):** 2-3 hours
- **Phase 5 (Low priority):** 1 hour
- **Phase 6 (Cleanup & QA):** 2 hours

**Total estimated time:** 10-15 hours

---

**Status:** Section 3 - Inventory Complete
**Next:** Begin Phase 1 migrations
