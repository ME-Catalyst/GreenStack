# GreenStack Repository Audit & Cleanup - Comprehensive Task List

> **Purpose:** Systematic audit and cleanup of the GreenStack repository to prepare for production deployment and public/professional release.
> **Output Location:** All audit outputs, reports, and documentation should be saved in `docs/audits/audit-baseline/`
> **Target:** Frontend documentation platform (`frontend/src/content/`) becomes the single source of truth.

**Last Updated:** 2025-11-25
**Status:** Not Started

---

## Task Completion Key

- [ ] Not Started
- [x] Completed
- [~] In Progress
- [!] Blocked/Issue

---

## 0. High-Level Objectives & Success Criteria

### Objectives
- [ ] Repository is safe and professional for public/client consumption
- [ ] Frontend documentation platform (`frontend/src/content/`) is the single source of truth
- [ ] All deprecated Markdown in `/docs/` is migrated or removed
- [ ] Dead code, backups, temp scripts, and internal notes are removed
- [ ] Root directory structure is minimal and follows conventions
- [ ] Complete system map exists: structure, dependencies, data flow, build/deploy
- [ ] Baseline documentation covers architecture, processes, and conventions
- [ ] Repository enables quick onboarding for new engineers

### Success Metrics
- [ ] Zero files with `.bak`, `.old`, `.tmp`, `.backup` extensions
- [ ] Zero TODO/HACK/FIXME comments without issue tracking
- [ ] All tests pass
- [ ] All linting passes
- [ ] CI/CD pipeline builds successfully
- [ ] Documentation coverage: 100% of core platform features documented

---

## 1. Pre-Audit Setup

### 1.1. Create Working Branch & Protection
- [ ] Create audit/cleanup branch: `chore/repo-audit-2025`
- [ ] Verify `main` branch protections:
  - [ ] No force pushes enabled
  - [ ] Require pull requests for merging
  - [ ] Require status checks to pass

### 1.2. Inventory and Tag Existing State
- [ ] Tag current main branch: `git tag pre-audit-baseline-20251125`
- [ ] Push tag to remote: `git push origin pre-audit-baseline-20251125`
- [ ] Generate repository structure snapshot:
  - [ ] Run: `tree -L 4 -I 'node_modules|__pycache__|.git|dist|build' > docs/audits/audit-baseline/repo-structure-pre-audit.txt`
  - [ ] Alternative: `ls -R > docs/audits/audit-baseline/repo-tree-pre-audit.txt`
- [ ] Create file count baseline:
  - [ ] Count all files: `find . -type f | wc -l > docs/audits/audit-baseline/file-count-pre.txt`
  - [ ] Count by extension: `find . -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn > docs/audits/audit-baseline/file-types-pre.txt`

### 1.3. Confirm Platform Conventions
- [ ] Document primary documentation path: `frontend/src/content/`
- [ ] Document deprecated documentation paths:
  - [ ] `docs/` - to be migrated or removed
  - [ ] Root-level `.md` files (except standard ones)
- [ ] Document build/deploy flow:
  - [ ] Frontend: Astro/Starlight build
  - [ ] Backend: Python/FastAPI
  - [ ] Database: SQLite (dev) / PostgreSQL (prod)
  - [ ] Deployment targets: TBD
- [ ] Create initial decisions document: `docs/audits/audit-baseline/platform-conventions.md`

**Output Files:**
- `docs/audits/audit-baseline/repo-structure-pre-audit.txt`
- `docs/audits/audit-baseline/file-count-pre.txt`
- `docs/audits/audit-baseline/file-types-pre.txt`
- `docs/audits/audit-baseline/platform-conventions.md`

---

## 2. Repository Structure & Root Cleanup

### 2.1. Root Files Audit

**Required/Recommended Root Files:**
- [ ] Audit `README.md`:
  - [ ] Verify high-level overview is accurate
  - [ ] Ensure getting started instructions work
  - [ ] Add badges (build status, license, etc.)
  - [ ] Link to deployed docs
- [ ] Audit or create `CONTRIBUTING.md`:
  - [ ] Coding standards
  - [ ] Branching strategy (Git flow)
  - [ ] PR process
  - [ ] Development setup reference
- [ ] Verify `LICENSE` file exists and is correct
- [ ] Create `CODE_OF_CONDUCT.md` if not exists (recommend Contributor Covenant)
- [ ] Create/audit `SECURITY.md`:
  - [ ] Vulnerability disclosure process
  - [ ] Security contact email
  - [ ] Supported versions
- [ ] Audit `CHANGELOG.md`:
  - [ ] Ensure format follows Keep a Changelog
  - [ ] Recent changes are documented
- [ ] Verify `.gitignore` is comprehensive:
  - [ ] Node modules
  - [ ] Python cache/venv
  - [ ] Database files (*.db, *.db-shm, *.db-wal)
  - [ ] Environment files (.env, .env.local)
  - [ ] Build artifacts
  - [ ] Editor configs (.vscode, .idea)
  - [ ] OS files (.DS_Store, Thumbs.db)

**Root Files to Review/Remove:**
- [ ] Identify all root `.md` files: `ls -la *.md`
- [ ] For each non-standard root markdown:
  - [ ] Evaluate relevance
  - [ ] Migrate to frontend docs if needed
  - [ ] Delete if obsolete
- [ ] Check for other root clutter:
  - [ ] Temp directories
  - [ ] Old scripts
  - [ ] Test data files
  - [ ] Backup files

### 2.2. Top-Level Directory Structure

**Expected Directories:**
- [ ] `frontend/` - Astro/Starlight documentation platform
- [ ] `backend/` or `src/` - Python backend services
- [ ] `scripts/` - Utility scripts (setup, backup, etc.)
- [ ] `alembic/` - Database migrations
- [ ] `config/` - Configuration files (Grafana, monitoring, etc.)
- [ ] `test-data/` - Sample IODD files and test fixtures
- [ ] `.github/` - GitHub Actions workflows
- [ ] `docs/` - TO BE MIGRATED/REMOVED

**Audit Each Top-Level Directory:**
- [ ] List all top-level directories: `ls -d */`
- [ ] Classify each directory:
  - [ ] `frontend/` - Application code ✓
  - [ ] `backend/` or `src/` - Application code ✓
  - [ ] `scripts/` - DevOps ✓
  - [ ] `alembic/` - Infrastructure ✓
  - [ ] `config/` - Infrastructure ✓
  - [ ] `test-data/` - Test fixtures ✓
  - [ ] `.github/` - CI/CD ✓
  - [ ] `docs/` - DEPRECATED (migrate to frontend)
  - [ ] Others: TBD

- [ ] For legacy/unclear directories:
  - [ ] Document purpose
  - [ ] Decide: Delete, Archive, or Promote
  - [ ] Execute decision

- [ ] Create `docs/audits/audit-baseline/repository-layout.md`:
  - [ ] Document final directory structure
  - [ ] Purpose of each directory
  - [ ] What belongs where

**Output Files:**
- `docs/audits/audit-baseline/root-files-audit.md`
- `docs/audits/audit-baseline/repository-layout.md`

---

## 3. Documentation Migration & Consolidation

### 3.1. Discovery of All Markdown Files

- [ ] Find all `.md` files in repository:
  ```bash
  find . -name "*.md" \
    -not -path "./node_modules/*" \
    -not -path "./.git/*" \
    -not -path "./frontend/node_modules/*" \
    > docs/audits/audit-baseline/all-markdown-files.txt
  ```

- [ ] Categorize by location:
  - [ ] Root level (`/*.md`)
  - [ ] `docs/**/*.md` (deprecated location)
  - [ ] `frontend/src/content/**/*.md` (canonical location)
  - [ ] Other locations

- [ ] Create inventory spreadsheet/document:
  - [ ] File path
  - [ ] Last modified date
  - [ ] Size
  - [ ] Status (Keep/Migrate/Delete)
  - [ ] Destination (if migrate)
  - [ ] Notes

### 3.2. Deduplication & Canonicalization

**Topics to Audit:**
- [ ] Architecture Overview
  - [ ] Find all architecture docs
  - [ ] Identify canonical version
  - [ ] Merge/consolidate if needed
- [ ] API Documentation
  - [ ] Find all API docs
  - [ ] Choose canonical location
  - [ ] Consolidate
- [ ] Deployment/Setup Guides
  - [ ] Find all deployment docs
  - [ ] Consolidate into single guide
- [ ] Development Guides
  - [ ] Find all dev setup docs
  - [ ] Consolidate
- [ ] PQA/IODD Processing Documentation
  - [ ] Find all parser/processing docs
  - [ ] Consolidate
- [ ] Database/Storage Documentation
  - [ ] Find all DB schema docs
  - [ ] Consolidate

**Process for Each Topic:**
- [ ] List all files covering this topic
- [ ] Identify most up-to-date version
- [ ] Choose canonical home in `frontend/src/content/`
- [ ] Merge content:
  - [ ] Preserve most accurate sections
  - [ ] Import missing details from older docs
  - [ ] Update terminology to match current codebase
  - [ ] Update code references to current paths
- [ ] Create migration tracking in: `docs/audits/audit-baseline/doc-migration-tracker.md`

### 3.3. Migration Execution

**For each file in `docs/` and other deprecated paths:**

- [ ] Review content relevance:
  - [ ] If irrelevant: DELETE
  - [ ] If partially relevant: EXTRACT useful parts → frontend docs, then DELETE
  - [ ] If fully relevant: MIGRATE to frontend docs

- [ ] Migration checklist for each document:
  - [ ] Convert to Starlight/Astro format
  - [ ] Add proper frontmatter (title, description, sidebar position)
  - [ ] Update internal links to new locations
  - [ ] Update code references
  - [ ] Add to sidebar navigation
  - [ ] Test rendering in dev server
  - [ ] Delete original file after migration

### 3.4. Frontend Documentation Quality Pass

**Required Documentation Pages** (create/update in `frontend/src/content/`):

Core Documentation:
- [ ] **Landing Page** (`index.md`)
  - [ ] Project overview
  - [ ] Key features
  - [ ] Quick start
  - [ ] Links to main sections

- [ ] **Architecture Overview** (`docs/architecture/`)
  - [ ] System architecture diagram
  - [ ] Component breakdown
  - [ ] Technology stack
  - [ ] Design decisions

- [ ] **Frontend Guide** (`docs/frontend/`)
  - [ ] Astro/Starlight overview
  - [ ] Content structure
  - [ ] Component usage
  - [ ] Styling/theming

- [ ] **Backend Guide** (`docs/backend/`)
  - [ ] FastAPI structure
  - [ ] API endpoints
  - [ ] Service layer
  - [ ] Data models

- [ ] **Database & Storage** (`docs/database/`)
  - [ ] Schema overview
  - [ ] Migrations (Alembic)
  - [ ] Storage manager
  - [ ] Query patterns

- [ ] **IODD Processing** (`docs/iodd/`)
  - [ ] Parser architecture
  - [ ] PQA generation
  - [ ] Supported formats
  - [ ] Extension points

- [ ] **Build & Deployment** (`docs/deployment/`)
  - [ ] Build process
  - [ ] Environment configuration
  - [ ] Deployment targets
  - [ ] CI/CD pipeline

- [ ] **Configuration & Secrets** (`docs/configuration/`)
  - [ ] Environment variables
  - [ ] Secret management
  - [ ] Configuration files
  - [ ] Environment-specific settings

- [ ] **Developer Setup** (`docs/development/setup.md`)
  - [ ] Prerequisites
  - [ ] Clone and install
  - [ ] Database setup
  - [ ] Running locally
  - [ ] Common issues

- [ ] **Testing Strategy** (`docs/development/testing.md`)
  - [ ] Test structure
  - [ ] Running tests
  - [ ] Writing tests
  - [ ] Coverage goals

- [ ] **Logging & Monitoring** (`docs/operations/monitoring.md`)
  - [ ] Logging configuration
  - [ ] Monitoring setup (Grafana/Prometheus)
  - [ ] Metrics and alerts
  - [ ] Debugging tips

- [ ] **API Reference** (`docs/api/`)
  - [ ] REST endpoints
  - [ ] Request/response formats
  - [ ] Authentication
  - [ ] Error codes

- [ ] **FAQ / Troubleshooting** (`docs/troubleshooting.md`)
  - [ ] Common issues
  - [ ] Error messages
  - [ ] Solutions and workarounds

**Quality Checks:**
- [ ] All pages use consistent heading structure
- [ ] Cross-links between related topics work
- [ ] Code examples are tested and current
- [ ] Diagrams are up to date
- [ ] Navigation/sidebar is logical
- [ ] Search works for key terms

**Output Files:**
- `docs/audits/audit-baseline/all-markdown-files.txt`
- `docs/audits/audit-baseline/doc-inventory.md`
- `docs/audits/audit-baseline/doc-migration-tracker.md`
- `docs/audits/audit-baseline/doc-deduplication-report.md`

---

## 4. Codebase Cleanup: Files, Dead Code, and Backups

### 4.1. Search for Backups, Temp Files, and Archives

**Find backup patterns:**
- [ ] Search for backup file extensions:
  ```bash
  find . -type f \( \
    -name "*~" -o \
    -name "*.bak" -o \
    -name "*.old" -o \
    -name "*.tmp" -o \
    -name "*.orig" -o \
    -name "*.copy" -o \
    -name "*.backup" \
  \) -not -path "./node_modules/*" -not -path "./.git/*" \
  > docs/audits/audit-baseline/backup-files-found.txt
  ```

- [ ] Search for backup/archive directories:
  ```bash
  find . -type d \( \
    -name "backup*" -o \
    -name "old" -o \
    -name "*_old" -o \
    -name "legacy" -o \
    -name "archive*" -o \
    -name "trash" -o \
    -name "DEPRECATED" -o \
    -name "z_*" \
  \) -not -path "./node_modules/*" -not -path "./.git/*" \
  > docs/audits/audit-baseline/archive-dirs-found.txt
  ```

- [ ] Search for common temp patterns:
  - [ ] `test_*.py` (unless in proper test directory)
  - [ ] `check_*.py` (ad-hoc scripts)
  - [ ] `*.db-wal`, `*.db-shm` (SQLite temp files)
  - [ ] Database backup files (e.g., `greenstack_backup_*.db`)

**Process each finding:**
- [ ] Review each backup file/directory
- [ ] Determine if preservation is needed (if yes, archive externally)
- [ ] Delete from repository
- [ ] Update `.gitignore` to prevent re-addition

### 4.2. Dead Code and Unused Assets

**Frontend (JavaScript/TypeScript):**
- [ ] Run ESLint for unused imports/variables
- [ ] Check for unused components:
  ```bash
  # List all .jsx/.tsx files and cross-reference imports
  ```
- [ ] Run bundle analyzer to find unused code:
  ```bash
  npm run build -- --analyze
  ```
- [ ] Identify unused CSS/styles
- [ ] Check for unused images/assets in `public/` or `assets/`

**Backend (Python):**
- [ ] Run Ruff or Flake8 for unused imports
- [ ] Search for unused modules:
  - [ ] Grep for imports in all Python files
  - [ ] Identify modules never imported
- [ ] Check for unused utility functions
- [ ] Identify deprecated API endpoints (check if called)

**Database:**
- [ ] Review Alembic migrations:
  - [ ] Check for orphaned migration files
  - [ ] Ensure migration history is clean
- [ ] Check for unused database tables/columns (compare schema to code usage)

**Scripts:**
- [ ] Review all scripts in `scripts/`:
  - [ ] Document purpose of each
  - [ ] Remove obsolete scripts
  - [ ] Ensure all scripts are documented

**Process:**
- [ ] For each unused item:
  - [ ] Verify it's truly unused (search all files)
  - [ ] Delete or refactor
  - [ ] Run tests after deletion
  - [ ] Run build after deletion

**Output Files:**
- `docs/audits/audit-baseline/backup-files-found.txt`
- `docs/audits/audit-baseline/archive-dirs-found.txt`
- `docs/audits/audit-baseline/dead-code-report.md`
- `docs/audits/audit-baseline/unused-assets-report.md`

---

## 5. Comment & Internal Notes Scrub

### 5.1. Comment Policy Definition

**Document comment policy in:** `docs/audits/audit-baseline/comment-policy.md`

**REMOVE these types of comments:**
- [ ] Internal incident references ("Hack from 2023-02 fix")
- [ ] Private context ("Ask Alice about this hack")
- [ ] Debugging leftovers ("HACK: temporary workaround" without explanation)
- [ ] Names of team members in casual context
- [ ] References to internal tools/systems not relevant to code
- [ ] Profanity or unprofessional language
- [ ] Commented-out code blocks (unless specifically needed with explanation)

**KEEP or ADD these comments:**
- [ ] Technical explanations of non-obvious implementations
- [ ] "Why" not "what" comments
- [ ] High-level module/class docstrings
- [ ] Complex algorithm explanations
- [ ] Performance notes
- [ ] Security considerations
- [ ] API contracts and usage notes

### 5.2. Systematic Comment Search

**Search for problematic keywords:**
- [ ] Search for `TODO`:
  ```bash
  grep -r "TODO" --include="*.py" --include="*.js" --include="*.jsx" --include="*.ts" --include="*.tsx" . \
    > docs/audits/audit-baseline/todos-found.txt
  ```

- [ ] Search for `FIXME`:
  ```bash
  grep -r "FIXME" --include="*.py" --include="*.js" --include="*.jsx" --include="*.ts" --include="*.tsx" . \
    > docs/audits/audit-baseline/fixmes-found.txt
  ```

- [ ] Search for `HACK`:
  ```bash
  grep -r "HACK" --include="*.py" --include="*.js" --include="*.jsx" --include="*.ts" --include="*.tsx" . \
    > docs/audits/audit-baseline/hacks-found.txt
  ```

- [ ] Search for `XXX`:
  ```bash
  grep -r "XXX" --include="*.py" --include="*.js" --include="*.jsx" --include="*.ts" --include="*.tsx" . \
    > docs/audits/audit-baseline/xxxs-found.txt
  ```

- [ ] Search for `DEBUG`:
  ```bash
  grep -r "DEBUG" --include="*.py" --include="*.js" --include="*.jsx" --include="*.ts" --include="*.tsx" . \
    > docs/audits/audit-baseline/debugs-found.txt
  ```

- [ ] Search for `TEMP`:
  ```bash
  grep -r "TEMP" --include="*.py" --include="*.js" --include="*.jsx" --include="*.ts" --include="*.tsx" . \
    > docs/audits/audit-baseline/temps-found.txt
  ```

**Process each finding:**
- [ ] For each TODO/FIXME:
  - [ ] If actionable: Create GitHub issue and reference in comment
  - [ ] If not actionable: Remove
  - [ ] If completed: Remove comment

- [ ] For each HACK/XXX/DEBUG/TEMP:
  - [ ] Evaluate if still needed
  - [ ] If needed: Rephrase professionally with technical justification
  - [ ] If not needed: Remove
  - [ ] Create issue for proper fix if hack is temporary

- [ ] Search for casual/internal language:
  - [ ] Names of people
  - [ ] Internal tool/system names
  - [ ] Casual phrases
  - [ ] Replace with professional, context-free language

**Output Files:**
- `docs/audits/audit-baseline/comment-policy.md`
- `docs/audits/audit-baseline/todos-found.txt`
- `docs/audits/audit-baseline/fixmes-found.txt`
- `docs/audits/audit-baseline/hacks-found.txt`
- `docs/audits/audit-baseline/comment-scrub-report.md`

---

## 6. Code Quality, Linting & Formatting

### 6.1. Tooling Inventory

**Frontend:**
- [ ] Identify linting tools:
  - [ ] ESLint configuration: `.eslintrc.*`
  - [ ] TypeScript config: `tsconfig.json`
- [ ] Identify formatting tools:
  - [ ] Prettier configuration: `.prettierrc.*`
- [ ] Document current rules and configurations

**Backend:**
- [ ] Identify linting tools:
  - [ ] Ruff/Flake8/Pylint configuration
  - [ ] MyPy for type checking: `pyproject.toml` or `mypy.ini`
- [ ] Identify formatting tools:
  - [ ] Black/Ruff formatter configuration
- [ ] Document current rules

**Create inventory:** `docs/audits/audit-baseline/code-quality-tools.md`

### 6.2. Normalize Code Style

**Frontend:**
- [ ] Agree on canonical JavaScript/TypeScript style
- [ ] Update ESLint rules if needed
- [ ] Update Prettier config if needed
- [ ] Run Prettier across codebase:
  ```bash
  npm run format
  # or
  npx prettier --write "frontend/src/**/*.{js,jsx,ts,tsx,astro,css}"
  ```
- [ ] Fix ESLint errors:
  ```bash
  npm run lint:fix
  ```
- [ ] Review remaining ESLint warnings
- [ ] Run TypeScript checks:
  ```bash
  npm run type-check
  ```

**Backend:**
- [ ] Agree on canonical Python style (recommend: Black with line length 100)
- [ ] Update Ruff/Black config if needed
- [ ] Run formatter across codebase:
  ```bash
  ruff format .
  # or
  black .
  ```
- [ ] Run linter:
  ```bash
  ruff check . --fix
  ```
- [ ] Fix remaining linting issues
- [ ] Run type checker:
  ```bash
  mypy src/
  ```

**Documentation:**
- [ ] Run markdownlint or similar
- [ ] Fix formatting issues

**Integration:**
- [ ] Add pre-commit hooks (optional):
  - [ ] Install pre-commit
  - [ ] Configure `.pre-commit-config.yaml`
  - [ ] Test hooks
- [ ] Update CI to enforce formatting/linting (see Section 8)

**Output Files:**
- `docs/audits/audit-baseline/code-quality-tools.md`
- `docs/audits/audit-baseline/style-guide.md`
- `docs/audits/audit-baseline/linting-report.md`

---

## 7. Architecture & Dependency Mapping

### 7.1. Component & Module Map

**Frontend Architecture:**
- [ ] List key modules/components:
  - [ ] Documentation platform (Starlight/Astro)
  - [ ] Content structure
  - [ ] Reusable components
  - [ ] Pages/routes
- [ ] Document internal dependencies
- [ ] Document external dependencies (npm packages)
- [ ] Create diagram: `docs/audits/audit-baseline/diagrams/frontend-architecture.md`

**Backend Architecture:**
- [ ] List key modules:
  - [ ] API layer (FastAPI routes)
  - [ ] Service layer (business logic)
  - [ ] Data layer (models, storage)
  - [ ] Parser layer (IODD/EDS/PQA)
  - [ ] Utility modules
- [ ] Document module responsibilities
- [ ] Document internal dependencies (who imports whom)
- [ ] Document external dependencies (pip packages)
- [ ] Create diagram: `docs/audits/audit-baseline/diagrams/backend-architecture.md`

**System Architecture:**
- [ ] Create high-level system diagram:
  - [ ] Frontend ↔ Backend communication
  - [ ] Backend ↔ Database
  - [ ] External file processing
  - [ ] Worker/queue system (if applicable)
- [ ] Document data flow:
  - [ ] File upload → Processing → Storage → Display
  - [ ] User interaction flows
- [ ] Save as: `docs/audits/audit-baseline/diagrams/system-architecture.md`

**Create Architecture Overview:**
- [ ] Write comprehensive architecture doc: `docs/audits/audit-baseline/architecture-overview.md`
- [ ] Include all diagrams
- [ ] Explain design decisions
- [ ] Document patterns used

### 7.2. Dependency Inventory

**Frontend Dependencies:**
- [ ] Review `frontend/package.json`:
  - [ ] List all dependencies
  - [ ] List all devDependencies
- [ ] For each dependency:
  - [ ] Verify it's used (search codebase for imports)
  - [ ] Note version and reason for inclusion
  - [ ] Check for security vulnerabilities: `npm audit`
  - [ ] Remove unused dependencies
  - [ ] Document critical dependencies

**Backend Dependencies:**
- [ ] Review dependency files:
  - [ ] `requirements.txt` or
  - [ ] `pyproject.toml` (Poetry/Ruff)
- [ ] For each dependency:
  - [ ] Verify it's used (search for imports)
  - [ ] Note version and reason for inclusion
  - [ ] Check for security vulnerabilities: `pip-audit` or `safety`
  - [ ] Remove unused dependencies
  - [ ] Document critical dependencies

**Dependency Documentation:**
- [ ] Create `docs/audits/audit-baseline/dependency-inventory.md`:
  - [ ] Frontend dependencies table
  - [ ] Backend dependencies table
  - [ ] Version pinning strategy
  - [ ] Update schedule
  - [ ] Security scanning process

**License Compliance:**
- [ ] Check licenses of all dependencies
- [ ] Ensure compatibility with project license
- [ ] Document any license concerns

**Output Files:**
- `docs/audits/audit-baseline/diagrams/frontend-architecture.md`
- `docs/audits/audit-baseline/diagrams/backend-architecture.md`
- `docs/audits/audit-baseline/diagrams/system-architecture.md`
- `docs/audits/audit-baseline/architecture-overview.md`
- `docs/audits/audit-baseline/dependency-inventory.md`
- `docs/audits/audit-baseline/dependency-licenses.md`

---

## 8. Build, Test & Deployment Pipeline

### 8.1. CI/CD Configuration Review

**GitHub Actions Workflows:**
- [ ] List all workflows in `.github/workflows/`:
  ```bash
  ls -la .github/workflows/
  ```
- [ ] For each workflow file:
  - [ ] Document purpose
  - [ ] Verify it's still needed
  - [ ] Remove obsolete workflows
  - [ ] Rename for clarity if needed

**Required Workflows:**
- [ ] **Linting & Formatting:**
  - [ ] Frontend: ESLint + Prettier
  - [ ] Backend: Ruff/Black
  - [ ] Fails on errors

- [ ] **Type Checking:**
  - [ ] TypeScript: `tsc --noEmit`
  - [ ] Python: `mypy`

- [ ] **Tests:**
  - [ ] Frontend tests (if any)
  - [ ] Backend tests (pytest)
  - [ ] Integration tests
  - [ ] Coverage reporting

- [ ] **Build:**
  - [ ] Frontend build (Astro)
  - [ ] Backend packaging (if needed)
  - [ ] Verify builds succeed

- [ ] **Security Scanning:**
  - [ ] Dependency vulnerability scanning
  - [ ] Secret scanning
  - [ ] SAST scanning (optional)

**Secrets Management:**
- [ ] Audit workflow files for hardcoded secrets
- [ ] Ensure only secret references are used (e.g., `${{ secrets.API_KEY }}`)
- [ ] Document required secrets in `docs/audits/audit-baseline/ci-secrets.md`

**Workflow Optimization:**
- [ ] Review caching strategy (npm cache, pip cache)
- [ ] Optimize job dependencies
- [ ] Ensure efficient resource usage

### 8.2. Build & Deploy Documentation

**Create Build & Deploy Guide:** `docs/audits/audit-baseline/build-deploy-guide.md`

Include:
- [ ] **Supported Environments:**
  - [ ] Development (local)
  - [ ] Staging (if applicable)
  - [ ] Production
  - [ ] Environment-specific configurations

- [ ] **Build Commands:**
  - [ ] Frontend build: `npm run build`
  - [ ] Backend packaging (if applicable)
  - [ ] Database migration: `alembic upgrade head`

- [ ] **Environment Variables:**
  - [ ] List all required env vars
  - [ ] Document default values
  - [ ] Reference `.env.example` or `.env.production.template`

- [ ] **Deployment Targets:**
  - [ ] Frontend hosting (Netlify/Vercel/Static host)
  - [ ] Backend hosting (Docker/VM/Cloud)
  - [ ] Database hosting

- [ ] **Deployment Process:**
  - [ ] Manual deployment steps
  - [ ] Automated deployment (if configured)
  - [ ] Rollback procedure

- [ ] **Database Migrations:**
  - [ ] How to run migrations
  - [ ] Migration best practices
  - [ ] Rollback procedure

- [ ] **Release Process:**
  - [ ] Version tagging
  - [ ] GitHub Releases
  - [ ] Changelog updates
  - [ ] Communication plan

**Output Files:**
- `docs/audits/audit-baseline/ci-workflow-inventory.md`
- `docs/audits/audit-baseline/ci-secrets.md`
- `docs/audits/audit-baseline/build-deploy-guide.md`

---

## 9. Security & Secrets Audit

### 9.1. Repository Secret Scanning

**Run Secret Scanning Tools:**
- [ ] Install secret scanning tool:
  - [ ] Option 1: `gitleaks` - `brew install gitleaks` or download binary
  - [ ] Option 2: `trufflehog` - `pip install trufflehog`
  - [ ] Option 3: `git-secrets` - `brew install git-secrets`

- [ ] Run scan:
  ```bash
  # Example with gitleaks
  gitleaks detect --source . --report-path docs/audits/audit-baseline/secret-scan-report.json
  ```

- [ ] Review scan results:
  - [ ] Check for API keys
  - [ ] Check for passwords
  - [ ] Check for tokens
  - [ ] Check for private keys
  - [ ] Check for database credentials

**Manual Checks:**
- [ ] Search for common patterns:
  ```bash
  grep -r "api_key\|API_KEY\|apiKey" --include="*.py" --include="*.js" --include="*.jsx" --include="*.ts" --include="*.tsx" --include="*.md" .
  grep -r "password\|PASSWORD\|passwd" --include="*.py" --include="*.js" --include="*.jsx" --include="*.ts" --include="*.tsx" --include="*.md" .
  grep -r "secret\|SECRET" --include="*.py" --include="*.js" --include="*.jsx" --include="*.ts" --include="*.tsx" --include="*.md" .
  grep -r "token\|TOKEN" --include="*.py" --include="*.js" --include="*.jsx" --include="*.ts" --include="*.tsx" --include="*.md" .
  ```

- [ ] Check specific files:
  - [ ] `.env` files (should not be in repo)
  - [ ] `.env.example` or `.env.template` (should have dummy values only)
  - [ ] Config files (`config/*.json`, `config/*.yaml`)
  - [ ] Test fixtures
  - [ ] Database seed files

**Remediation:**
- [ ] For each leaked secret found:
  - [ ] IMMEDIATELY rotate/revoke the secret externally
  - [ ] Remove from codebase
  - [ ] Add to `.gitignore` if file-based
  - [ ] Consider using `git filter-branch` or `BFG Repo-Cleaner` to remove from history
  - [ ] Document incident in `docs/audits/audit-baseline/secret-leaks-remediated.md`

### 9.2. Secure-by-Default Configuration

**Environment File Templates:**
- [ ] Audit `.env.example` or `.env.production.template`:
  - [ ] Ensure all values are placeholders or safe defaults
  - [ ] No real secrets
  - [ ] Clear comments for each variable

- [ ] Create comprehensive `.env.example`:
  - [ ] All required variables listed
  - [ ] Comments explaining purpose
  - [ ] Example safe values

**Configuration Files:**
- [ ] Audit all config files in `config/`:
  - [ ] No hardcoded secrets
  - [ ] Environment variable references only
  - [ ] Document in code comments

**Documentation:**
- [ ] Create/update `SECURITY.md`:
  - [ ] Vulnerability disclosure policy
  - [ ] Security contact email
  - [ ] Supported versions
  - [ ] Known security considerations

- [ ] Document secrets management:
  - [ ] Where secrets should be stored
  - [ ] How to configure secrets in each environment
  - [ ] Rotation policy

**Security Best Practices Check:**
- [ ] Input validation in API endpoints
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (output escaping)
- [ ] CSRF protection (if applicable)
- [ ] Authentication and authorization implementation
- [ ] File upload restrictions
- [ ] Rate limiting (if applicable)

**Output Files:**
- `docs/audits/audit-baseline/secret-scan-report.json`
- `docs/audits/audit-baseline/secret-leaks-remediated.md`
- `docs/audits/audit-baseline/security-audit-report.md`
- `docs/audits/audit-baseline/secrets-management-guide.md`

---

## 10. Final Documentation Pass in Frontend Content

### 10.1. Required Documentation Pages

**Migrate/create these pages in `frontend/src/content/`:**

- [ ] **Project Overview** (`index.md` or `docs/overview.md`)
  - [ ] What is GreenStack
  - [ ] Key features
  - [ ] Use cases
  - [ ] Technology overview

- [ ] **Architecture Overview** (`docs/architecture/overview.md`)
  - [ ] System architecture diagram
  - [ ] Component breakdown
  - [ ] Technology stack
  - [ ] Design principles
  - [ ] Data flow

- [ ] **Repository Layout** (`docs/architecture/repository-layout.md`)
  - [ ] Directory structure
  - [ ] Purpose of each directory
  - [ ] File organization conventions
  - [ ] Where to add new code

- [ ] **Development Setup** (`docs/development/setup.md`)
  - [ ] Prerequisites (Node, Python, etc.)
  - [ ] Clone repository
  - [ ] Install dependencies
  - [ ] Database setup
  - [ ] Environment configuration
  - [ ] Run locally
  - [ ] Verify installation

- [ ] **Coding Standards & Conventions** (`docs/development/conventions.md`)
  - [ ] Code style guides
  - [ ] Naming conventions
  - [ ] File organization
  - [ ] Import ordering
  - [ ] Documentation requirements
  - [ ] Git commit message format
  - [ ] Branch naming

- [ ] **Build & Deployment Guide** (`docs/deployment/guide.md`)
  - [ ] Build process
  - [ ] Environment configuration
  - [ ] Deployment to each environment
  - [ ] Database migrations
  - [ ] Release process
  - [ ] Rollback procedure

- [ ] **Dependency Overview** (`docs/architecture/dependencies.md`)
  - [ ] Frontend dependencies
  - [ ] Backend dependencies
  - [ ] Rationale for major dependencies
  - [ ] Version management
  - [ ] Update process

- [ ] **Testing Strategy** (`docs/development/testing.md`)
  - [ ] Test structure
  - [ ] Running tests
  - [ ] Writing new tests
  - [ ] Test coverage
  - [ ] CI integration

- [ ] **Logging & Monitoring** (`docs/operations/monitoring.md`)
  - [ ] Logging setup
  - [ ] Log levels
  - [ ] Monitoring with Grafana/Prometheus
  - [ ] Key metrics
  - [ ] Alerts
  - [ ] Debugging guide

- [ ] **FAQ / Troubleshooting** (`docs/troubleshooting.md`)
  - [ ] Common setup issues
  - [ ] Build errors
  - [ ] Runtime errors
  - [ ] Database issues
  - [ ] Performance issues

- [ ] **Changelog** (`docs/changelog.md` or link to `CHANGELOG.md`)
  - [ ] Recent changes
  - [ ] Version history
  - [ ] Breaking changes

- [ ] **API Reference** (`docs/api/reference.md`)
  - [ ] REST endpoints
  - [ ] Request/response formats
  - [ ] Authentication
  - [ ] Error codes
  - [ ] Examples

- [ ] **IODD Processing Guide** (`docs/features/iodd-processing.md`)
  - [ ] IODD parser overview
  - [ ] PQA generation
  - [ ] Supported formats
  - [ ] Extension guide
  - [ ] Troubleshooting

### 10.2. Documentation Quality Checklist

For each documentation page:
- [ ] **Structure:**
  - [ ] Clear title and description
  - [ ] Logical heading hierarchy (H1 → H2 → H3)
  - [ ] Table of contents if long

- [ ] **Content:**
  - [ ] Accurate and up-to-date
  - [ ] No broken references to removed code/files
  - [ ] Code examples are tested and work
  - [ ] Commands are verified

- [ ] **Linking:**
  - [ ] Internal links work (to other docs)
  - [ ] External links work
  - [ ] Cross-references are relevant

- [ ] **Navigation:**
  - [ ] Appears in sidebar
  - [ ] Correct position in hierarchy
  - [ ] Breadcrumbs work

- [ ] **Rendering:**
  - [ ] Test in dev server
  - [ ] Code blocks have correct syntax highlighting
  - [ ] Diagrams render correctly
  - [ ] No broken images

### 10.3. Documentation Site Configuration

- [ ] Update `astro.config.mjs` or equivalent:
  - [ ] Site title
  - [ ] Site description
  - [ ] Social links
  - [ ] Logo/branding

- [ ] Update sidebar configuration:
  - [ ] Logical grouping
  - [ ] Clear labels
  - [ ] Proper ordering

- [ ] Configure search:
  - [ ] Verify search is enabled
  - [ ] Test key term searches

- [ ] Configure theme/styling:
  - [ ] Brand colors
  - [ ] Custom components
  - [ ] Responsive design

**Output Files:**
- All documentation should be in `frontend/src/content/`
- `docs/audits/audit-baseline/documentation-coverage-report.md`

---

## 11. Final Review & Sign-Off

### 11.1. Technical Validation

**Run Full Test Suite:**
- [ ] Frontend tests:
  ```bash
  cd frontend
  npm test
  ```
- [ ] Backend tests:
  ```bash
  pytest
  ```
- [ ] Integration tests (if any)
- [ ] Verify all tests pass
- [ ] Check test coverage meets targets

**Run Full Build:**
- [ ] Frontend build:
  ```bash
  cd frontend
  npm run build
  ```
- [ ] Backend build/package (if applicable)
- [ ] Verify no build errors
- [ ] Verify no build warnings (or document expected ones)

**Run All Static Checks:**
- [ ] Frontend linting: `npm run lint`
- [ ] Frontend type checking: `npm run type-check`
- [ ] Backend linting: `ruff check .`
- [ ] Backend type checking: `mypy src/`
- [ ] Verify all checks pass

**Manual Smoke Testing:**
- [ ] Start frontend dev server and verify:
  - [ ] Homepage loads
  - [ ] Navigation works
  - [ ] Documentation pages render
  - [ ] Search works
  - [ ] No console errors

- [ ] Start backend dev server and verify:
  - [ ] API responds
  - [ ] Key endpoints work
  - [ ] Database connection works
  - [ ] No runtime errors

### 11.2. Documentation Validation

**Legacy Documentation Check:**
- [ ] Verify all files in `docs/` have been:
  - [ ] Migrated to `frontend/src/content/`, OR
  - [ ] Consciously deleted as obsolete
- [ ] No orphaned documentation remains
- [ ] Create final report: `docs/audits/audit-baseline/legacy-docs-final-report.md`

**Content Accuracy Check:**
- [ ] Spot-check docs for:
  - [ ] Outdated references (old service names, removed components)
  - [ ] Broken links
  - [ ] Incorrect code examples
  - [ ] Outdated screenshots/diagrams

**Navigation Check:**
- [ ] Verify sidebar navigation is logical
- [ ] All important pages are reachable
- [ ] URLs/slugs are clean and professional
- [ ] Breadcrumbs work correctly

### 11.3. Repository Hygiene Final Checklist

**Root Directory:**
- [ ] No deprecated folders in root
- [ ] No backup/temp files
- [ ] Only standard root markdown files
- [ ] `.gitignore` is comprehensive
- [ ] All root files serve a purpose

**Codebase:**
- [ ] No internal-sensitive comments
- [ ] No TODO/HACK without issue tracking
- [ ] Code style is consistent
- [ ] No dead code
- [ ] No unused imports

**Documentation:**
- [ ] Single source of truth (frontend docs)
- [ ] Complete coverage of core features
- [ ] Professional and clear
- [ ] Up-to-date with code

**Security:**
- [ ] No secrets in repository
- [ ] `.env.example` has safe defaults
- [ ] `SECURITY.md` exists
- [ ] Dependencies scanned for vulnerabilities

**CI/CD:**
- [ ] All workflows work
- [ ] Builds are green
- [ ] Tests pass
- [ ] Linting passes

### 11.4. Final Reports & Metrics

**Generate Completion Reports:**
- [ ] Create `docs/audits/audit-baseline/AUDIT_COMPLETION_REPORT.md`:
  - [ ] Summary of work completed
  - [ ] Files deleted count
  - [ ] Files migrated count
  - [ ] Issues found and resolved
  - [ ] Outstanding issues (if any)
  - [ ] Recommendations for ongoing maintenance

- [ ] Create metrics comparison:
  - [ ] Files before/after count
  - [ ] Code lines before/after
  - [ ] Test coverage before/after
  - [ ] Lint errors before/after

- [ ] Document lessons learned:
  - [ ] What went well
  - [ ] What was challenging
  - [ ] Process improvements for next audit

### 11.5. Merge & Tag

**Prepare for Merge:**
- [ ] Ensure all checklist items above are complete
- [ ] Commit all changes on audit branch
- [ ] Push audit branch to remote
- [ ] Review all changes in diff

**Create Pull Request:**
- [ ] Create PR from `chore/repo-audit-2025` to `main`
- [ ] Write comprehensive PR description:
  - [ ] Summary of changes
  - [ ] Link to audit task list
  - [ ] Link to completion report
  - [ ] Breaking changes (if any)
  - [ ] Migration notes (if any)
- [ ] Request review (if applicable)
- [ ] Address review feedback

**Merge:**
- [ ] Ensure CI passes on PR
- [ ] Merge PR to main (squash or merge commit, per team preference)
- [ ] Delete audit branch after merge

**Tag Release:**
- [ ] Tag the merge commit:
  ```bash
  git tag -a v1.0.0-audit-baseline -m "Post-audit baseline release"
  git push origin v1.0.0-audit-baseline
  ```

- [ ] Create GitHub Release:
  - [ ] Title: "v1.0.0 - Post-Audit Baseline"
  - [ ] Description: Summary of audit and cleanup
  - [ ] Link to completion report
  - [ ] Attach any relevant artifacts

**Communication:**
- [ ] Announce completion to team
- [ ] Document new onboarding process
- [ ] Update contribution guide if needed

---

## Ongoing Maintenance

**Establish Regular Reviews:**
- [ ] Schedule quarterly documentation reviews
- [ ] Schedule monthly dependency updates
- [ ] Schedule quarterly security scans
- [ ] Create maintenance runbook: `docs/audits/audit-baseline/maintenance-runbook.md`

**Prevent Regression:**
- [ ] Add pre-commit hooks for:
  - [ ] Formatting
  - [ ] Linting
  - [ ] Secret scanning
- [ ] Update CI to enforce standards
- [ ] Document code review checklist
- [ ] Create new contributor onboarding guide

---

## Appendix: File Output Summary

All audit outputs should be saved in `docs/audits/audit-baseline/`:

```
docs/audits/audit-baseline/
├── TASK_LIST.md (this file)
├── AUDIT_COMPLETION_REPORT.md
├── repo-structure-pre-audit.txt
├── file-count-pre.txt
├── file-types-pre.txt
├── platform-conventions.md
├── repository-layout.md
├── root-files-audit.md
├── all-markdown-files.txt
├── doc-inventory.md
├── doc-migration-tracker.md
├── doc-deduplication-report.md
├── backup-files-found.txt
├── archive-dirs-found.txt
├── dead-code-report.md
├── unused-assets-report.md
├── comment-policy.md
├── todos-found.txt
├── fixmes-found.txt
├── hacks-found.txt
├── comment-scrub-report.md
├── code-quality-tools.md
├── style-guide.md
├── linting-report.md
├── dependency-inventory.md
├── dependency-licenses.md
├── ci-workflow-inventory.md
├── ci-secrets.md
├── build-deploy-guide.md
├── secret-scan-report.json
├── secret-leaks-remediated.md
├── security-audit-report.md
├── secrets-management-guide.md
├── documentation-coverage-report.md
├── legacy-docs-final-report.md
├── maintenance-runbook.md
└── diagrams/
    ├── frontend-architecture.md
    ├── backend-architecture.md
    └── system-architecture.md
```

---

**End of Task List**
