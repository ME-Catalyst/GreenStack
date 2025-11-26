# Repository Audit & Cleanup Plan

> **Purpose:** This document is a reusable, detailed checklist and process guide for auditing, cleaning, and preparing a GitHub repository for public release and/or production deployment.  
> It assumes:
> - Primary documentation lives in a frontend content system (e.g. `frontend/src/content`).
> - Legacy Markdown docs may exist in `docs/` or elsewhere and must be migrated or removed.
> - Internal notes, backups, and dead code should not ship in the public repo.

You can adapt paths, names, and details to any project by adjusting the examples and TODO markers.

---

## 0. High-Level Objectives

- Ensure the repository is **safe and professional** for public consumption.
- Make the **frontend documentation platform** (e.g. `frontend/src/content`) the single source of truth.
- Remove or archive **deprecated Markdown** (e.g. `/docs/`, scratch notes, etc.).
- Remove **dead code**, **backups**, **temporary scripts**, and **internal fixes/notes** from the shipped code.
- Structure the root of the repo to be **minimal and conventional**.
- Produce a **clear map** of the codebase: structure, dependencies, data flow, and build/deploy process.
- Create **baseline documentation** in the frontend doc platform covering architecture, processes, and conventions.
- Leave the repo in a state where a new engineer can onboard quickly and a reviewer can understand the system.

---

## 1. Pre-Audit Setup

### 1.1. Create a Working Branch

- [ ] Create a long-lived audit/cleanup branch:
  - Name suggestion: `chore/repo-audit-cleanup`.
- [ ] Protect `main` / `master` as needed (no force pushes, require PRs).

### 1.2. Inventory and Tag Existing State

- [ ] Tag the current main branch as a baseline before cleanup:
  - Example: `git tag pre-cleanup-YYYYMMDD`
- [ ] Generate a quick tree snapshot of the repo for reference (optional):
  - `tree -L 3 > repo-structure-pre-cleanup.txt`

### 1.3. Confirm Platform Conventions

- [ ] Confirm **primary documentation path** (e.g. `frontend/src/content`).
- [ ] Confirm **deprecated documentation path(s)** (e.g. `docs/`, `notes/`, `design/`).  
- [ ] Confirm **build/deploy** flow (CI provider, hosting, packaging, etc.).

Document any decisions in a working doc (to be later migrated to frontend docs).

---

## 2. Repository Structure & Root Cleanup

Goal: Keep the root as clean and conventional as possible.

### 2.1. Root Files: Keep vs Remove

**Required / Recommended root files (rename/adapt as needed):**

- [ ] `README.md` – High-level project overview and getting started.
- [ ] `CONTRIBUTING.md` – How to contribute, coding standards, branching strategy.
- [ ] `LICENSE` – Legal license for open-source or internal use.
- [ ] `CODE_OF_CONDUCT.md` – Optional but recommended for public repos.
- [ ] `SECURITY.md` – Security contact and vulnerability disclosure process.
- [ ] `CHANGELOG.md` – Optional but helpful for releases.
- [ ] `.gitignore` – Properly configured.
- [ ] Optional: `ARCHITECTURE.md` **only if** not duplicated in frontend docs (or just link to frontend docs).

**Tasks:**

- [ ] Audit all root `.md` files:
  - [ ] Keep only best-practice minimum set listed above.
  - [ ] For any other root markdown (e.g. `TODO.md`, `DEV_NOTES.md`):
    - [ ] Either delete after migration
    - **or**
    - [ ] Migrate relevant content into frontend docs (see Section 3).  
- [ ] Remove or relocate non-essential root files (e.g. `scratch/`, `old/`, `backup/`, large example datasets).
- [ ] Ensure root file naming is consistent and professional.

### 2.2. Folder Layout

- [ ] Identify all **top-level directories** and classify them:
  - Application code (e.g. `frontend/`, `backend/`, `services/`)
  - Infrastructure / DevOps (e.g. `.github/`, `deploy/`, `infra/`)
  - Documentation (e.g. `frontend/src/content/`, `docs/`)
  - Legacy / unclear (e.g. `old/`, `sandbox/`, `tmp/`)
- [ ] For each legacy/unclassified directory:
  - [ ] Decide: **Delete**, **Archive elsewhere**, or **Promote** to first-class (with docs).
  - [ ] If archived, create a clear archive folder (e.g. `archive/`), or better: archive in a separate repo if needed.

Document final structure in a **“Repository layout”** doc in frontend content.

---

## 3. Documentation Migration & Consolidation

Goal: `frontend/src/content` (or equivalent) is the **only** source of documentation truth.

### 3.1. Discovery of Markdown Files

- [ ] List all `.md` files in the repo:
  - `find . -name "*.md" -not -path "./node_modules/*" -not -path "./.git/*" > md-files.txt`
- [ ] Categorize MD files by location:
  - [ ] Root (`/*.md`)
  - [ ] `docs/**/*.md` (deprecated)
  - [ ] `frontend/src/content/**/*.md` (preferred)
  - [ ] Any others (`notes/`, `design/`, etc.).

### 3.2. Deduplication & Canonicalization

For each logical document topic (e.g. “Architecture Overview”, “API Reference”, “Deployment”):

- [ ] Identify duplicates / near-duplicates across:
  - `docs/`
  - `frontend/src/content/`
  - other locations.
- [ ] Choose a **canonical home** for each topic in `frontend/src/content`.
- [ ] Merge contents where needed:
  - [ ] Preserve **most up-to-date and accurate** sections.
  - [ ] Import missing details from older docs.
  - [ ] Update terminology and links to current architecture and code.

### 3.3. Migration Process

For each MD file in `docs/` or other deprecated paths:

- [ ] Confirm if content is still relevant.
  - [ ] **If irrelevant**: delete the file.
  - [ ] **If partially relevant**: move only the useful fragments into existing frontend docs and delete original.
  - [ ] **If fully relevant but not duplicated**: convert/migrate it to `frontend/src/content`.
- [ ] Ensure that migrated documents:
  - [ ] Follow the **documentation platform conventions** (front matter, component usage, etc.).
  - [ ] Have consistent title, slug/route, and sidebar navigation.
  - [ ] Include cross-links to related docs.

### 3.4. Documentation Quality Pass

For core docs in `frontend/src/content`:

- [ ] Ensure coverage of the following minimum set:

  - [ ] **Overview / Landing Page**
  - [ ] **Architecture Overview** (high-level system and components)
  - [ ] **Frontend Overview**
  - [ ] **Backend/Services Overview** (if applicable)
  - [ ] **Data & Storage (DB, queues, caches, etc.)**
  - [ ] **Build & Deployment**
  - [ ] **Configuration & Secrets Management**
  - [ ] **Environments** (dev/stage/prod)
  - [ ] **Developer Setup & Local Dev Guide**
  - [ ] **Testing Strategy & How to Run Tests**
  - [ ] **Logging, Monitoring, and Observability**
  - [ ] **FAQ / Troubleshooting**

- [ ] Clarify versioning where relevant (docs should match the current code version).

---

## 4. Codebase Cleanup: Files, Dead Code, and Backups

Goal: Ship only what’s needed for production and active development.

### 4.1. Search for Backups, Temp Files, and Archives

- [ ] Find common backup patterns:
  - Files ending in `~`, `.bak`, `.old`, `.tmp`, `.orig`, `.copy`, `.backup`.
  - Directories like `backup/`, `old/`, `z_old/`, `legacy/`, `trash/`, `DEPRECATED/`.
- [ ] For each:
  - [ ] Decide if anything needs to be preserved in a **separate archival location** (not in primary repo).
  - [ ] Remove from the repository or move to an `archive/` folder that is clearly out-of-scope for builds/tests.
  - [ ] Update `.gitignore` if necessary to avoid re-adding ephemeral files.

### 4.2. Dead Code and Unused Assets

- [ ] Identify unused:
  - Components
  - Modules
  - Scripts
  - Stylesheets
  - Images/assets
- [ ] Use tooling where possible:
  - Tree-shaking reports
  - Bundle analyzers
  - Static analysis (e.g. ESLint/TS ESLint, Python linters, etc.)
- [ ] Remove or refactor:
  - [ ] Delete truly unused modules.
  - [ ] Inline or merge duplicated logic.
  - [ ] Extract common utilities where relevant.
- [ ] Ensure that removing code doesn’t break tests or build:
  - [ ] Run the full test suite after major removals.
  - [ ] Run the full build and smoke tests.

---

## 5. Comment & Internal Notes Scrub

Goal: Remove internal-sensitive notes while keeping **high-quality technical comments**.

### 5.1. Policy for Comments

- **Remove**:
  - [ ] Comments mentioning specific internal incidents (“Hack from 2023-02 fix”).
  - [ ] TODOs/notes that reference private internal context (“Ask Alice about this hack”).
  - [ ] Debugging leftovers (“HACK: temporary workaround”).

- **Keep or Add** when useful:
  - [ ] Comments that explain **why** something is implemented in a non-obvious way.
  - [ ] High-level docstrings/JSDoc/Pydoc explaining module purpose and contract.
  - [ ] Usage notes for complex functions/classes.

### 5.2. Systematic Comment Pass

- [ ] Search for keywords in the codebase:
  - `TODO`, `FIXME`, `HACK`, `XXX`, `DEBUG`, `TEMP`, `WORKAROUND`.
- [ ] For each occurrence:
  - [ ] Decide: implement, clarify, or remove.
  - [ ] If still needed:
    - [ ] Rephrase to be professional and timeless.
    - [ ] Create an issue in the tracker for genuine TODOs and link issue ID.
- [ ] Search for casual/internal language in comments and docs (e.g., names, internal systems, offhand remarks) and clean them up.

---

## 6. Code Quality, Linting & Formatting

Goal: Codebase is consistent, readable, and enforceably formatted.

### 6.1. Tooling Inventory

- [ ] Identify existing tools:
  - Linting (`eslint`, `flake8`, `ruff`, etc.)
  - Formatting (`prettier`, `black`, etc.)
  - Type checking (`tsc`, `mypy`, etc.)
- [ ] Ensure configuration files are present and current:
  - `.eslintrc.*`
  - `.prettierrc.*`
  - `pyproject.toml` / `setup.cfg` / etc.

### 6.2. Normalize Code Style

- [ ] Agree on **canonical style** for each language.
- [ ] Run auto-formatters across the codebase.
- [ ] Fix lint errors or update rules to reflect current conventions.
- [ ] Integrate checks into CI (see Section 8).

---

## 7. Architecture & Dependency Mapping

Goal: Create a clear understanding of how everything fits together and document it in frontend content.

### 7.1. Component & Module Map

- [ ] For each major subsystem (e.g. frontend, backend services, workers):
  - [ ] List key modules/components and their responsibilities.
  - [ ] Note internal dependencies (who calls whom).
  - [ ] Note external dependencies (libraries, services, APIs).

- [ ] Create diagrams (can be stored in `frontend/src/content` or referenced):
  - High-level system architecture
  - Frontend routing and key views
  - Backend service topology (if applicable)
  - Data flow and main queues/DBs

### 7.2. Dependency Inventory

- [ ] Review dependency manifests:
  - `package.json`, `requirements.txt`, `pyproject.toml`, `go.mod`, etc.
- [ ] For each dependency:
  - [ ] Check if it is still used.
  - [ ] Remove unused dependencies.
  - [ ] Note critical dependencies (e.g. SDKs, core frameworks) in architecture docs.
  - [ ] Consider pinning or ranges for versions and document rationale.

Update `frontend/src/content` with a **Dependency Overview** page summarizing this.

---

## 8. Build, Test & Deployment Pipeline

Goal: A reviewer can understand exactly how the project is built, tested, and deployed.

### 8.1. CI/CD Configuration Review

- [ ] Audit `.github/workflows/` or equivalent CI pipelines:
  - [ ] Remove obsolete workflows.
  - [ ] Rename workflows for clarity.
  - [ ] Ensure workflows:
    - Install dependencies efficiently.
    - Run linters and tests.
    - Build artifacts (if applicable).
    - Optionally run security scans.

- [ ] Ensure secrets are **not** in the repo (only environment/secret references).

### 8.2. Build & Deploy Docs

Create or update a **Build & Deploy** doc in `frontend/src/content`:

- [ ] Supported environments (dev, staging, prod).
- [ ] Build commands and tools.
- [ ] How to configure environment variables.
- [ ] Hosting/deployment targets (e.g. Vercel, Netlify, Docker/Kubernetes, on-prem).
- [ ] How to run migrations, if any.
- [ ] Release process (tags, GitHub Releases, changelog updates).

---

## 9. Security & Secrets Audit

Goal: Ensure no secrets or sensitive data are present and basic security posture is documented.

### 9.1. Repository Scan

- [ ] Run secret scanning tools (e.g. `git-secrets`, `trufflehog`, `gitleaks`).
- [ ] Check:
  - `.env` files, config samples, test fixtures.
  - Any hard-coded tokens, passwords, or keys in code or docs.
- [ ] Replace any leaked secrets immediately and rotate them externally.

### 9.2. Secure-by-Default Config

- [ ] Confirm that sample configs (e.g. `.env.example`) are safe to publish.
- [ ] Clarify in docs what must be private and how to configure secrets.
- [ ] Ensure `SECURITY.md` describes how to report vulnerabilities.

---

## 10. Final Documentation Pass in Frontend Content

Goal: Use the frontend documentation platform as the canonical source of project knowledge.

Create/update the following pages in `frontend/src/content` (or equivalent):

- [ ] **Project Overview**
- [ ] **Architecture Overview**
- [ ] **Repository Layout**
- [ ] **Development Setup**
- [ ] **Coding Standards & Conventions**
- [ ] **Build & Deployment Guide**
- [ ] **Dependency Overview**
- [ ] **Testing Strategy**
- [ ] **Logging & Monitoring**
- [ ] **FAQ / Troubleshooting**
- [ ] **Changelog (or link to `CHANGELOG.md`)**

Each page should:

- [ ] Use consistent headings and structure.
- [ ] Cross-link related topics.
- [ ] Reference specific code modules or config files where relevant.
- [ ] Reflect the **post-cleanup** state of the repo.

---

## 11. Final Review & Sign-Off

### 11.1. Technical Review

- [ ] Run full test suite.
- [ ] Run full build.
- [ ] Run linting and static checks.
- [ ] Sanity-check main flows manually (click through critical UI paths, key API calls).

### 11.2. Documentation Review

- [ ] Validate that all important legacy docs from `docs/` and other locations have either:
  - [ ] Been migrated to `frontend/src/content`, or
  - [ ] Been consciously removed as no longer relevant.
- [ ] Spot-check for outdated references (old service names, removed components).
- [ ] Ensure navigation and URLs in the docs are coherent.

### 11.3. Repo Hygiene Checklist

- [ ] No obviously deprecated or cryptically named folders in root.
- [ ] No backup/temp files.
- [ ] No internal-sensitive comments or notes.
- [ ] Standard root files are present and accurate.
- [ ] CI builds green on the cleanup branch.

### 11.4. Merge & Tag

- [ ] Merge `chore/repo-audit-cleanup` into `main` via PR.
- [ ] Tag a new release:
  - Example: `vX.Y.0` – “Post-cleanup baseline release”.
- [ ] Optionally publish a **Release Notes** entry summarizing the cleanup.

---
