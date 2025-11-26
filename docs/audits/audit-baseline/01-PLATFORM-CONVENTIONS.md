# GreenStack Platform Conventions

**Date:** 2025-11-25
**Status:** Baseline Documentation
**Purpose:** Define canonical conventions, paths, and technical decisions for GreenStack

---

## 1. Documentation Conventions

### Primary Documentation Path
**Canonical Location:** `frontend/src/content/`

**Platform:** Astro with Starlight theme
- Static site generator for documentation
- Markdown/MDX files with frontmatter
- Component support for interactive elements
- Built-in search and navigation

**Structure:**
```
frontend/src/content/
├── docs/                    # Main documentation
│   ├── architecture/        # System architecture docs
│   ├── development/         # Developer guides
│   ├── deployment/          # Build and deploy guides
│   ├── api/                 # API reference
│   ├── features/            # Feature documentation
│   └── operations/          # Ops and monitoring
├── guides/                  # Tutorial-style guides
└── reference/               # Reference material
```

### Deprecated Documentation Paths
**To be migrated or removed:**
- `docs/` - Root-level docs directory (DEPRECATED)
- `*.md` in project root (except standard files)
- Any inline documentation scattered in code directories

**Standard Root Files (KEEP):**
- `README.md` - Project overview and getting started
- `CONTRIBUTING.md` - Contribution guidelines
- `LICENSE` - Legal license
- `CODE_OF_CONDUCT.md` - Community standards
- `SECURITY.md` - Security policy
- `CHANGELOG.md` - Version history

---

## 2. Technology Stack

### Frontend
**Documentation Platform:**
- **Framework:** Astro v4.x
- **Theme:** Starlight
- **Language:** JavaScript/TypeScript (JSX/TSX)
- **Styling:** Tailwind CSS (if applicable) / Starlight defaults
- **Package Manager:** npm

**Build Output:** Static HTML/CSS/JS

### Backend
**API & Services:**
- **Framework:** FastAPI (Python)
- **Language:** Python 3.11+
- **ASGI Server:** Uvicorn
- **Type Checking:** MyPy (strict mode)
- **Package Manager:** pip / poetry / ruff

**Key Modules:**
- API routes (`src/api/` or `backend/api/`)
- Service layer (business logic)
- Data models (SQLAlchemy or similar)
- Parser layer (IODD/EDS/PQA processing)
- Storage manager (file and data persistence)

### Database
**Development:**
- **Primary:** SQLite (`greenstack.db`)
- **Migrations:** Alembic
- **ORM:** SQLAlchemy

**Production:**
- **Primary:** PostgreSQL (recommended)
- **Migrations:** Alembic
- **Connection Pooling:** As needed

### Storage
**File Storage:**
- IODD files (XML)
- EDS files
- Generated PQA files
- Device images and icons

**Storage Location:**
- Development: Local filesystem
- Production: TBD (filesystem, S3, or similar)

---

## 3. Build & Deploy Flow

### Frontend (Documentation Site)

**Development:**
```bash
cd frontend
npm install
npm run dev
# Runs on http://localhost:4321
```

**Build:**
```bash
npm run build
# Output: frontend/dist/
```

**Deployment:**
- **Platform:** TBD (Netlify, Vercel, GitHub Pages, or static hosting)
- **Process:** Manual or automated via CI/CD
- **URL:** TBD

### Backend (API Services)

**Development:**
```bash
# Setup virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start server
uvicorn src.main:app --reload
# Runs on http://localhost:8000
```

**Build/Package:**
- Docker containerization (optional)
- Python package (wheel/sdist)

**Deployment:**
- **Platform:** TBD (Docker, VM, cloud platform)
- **Database:** PostgreSQL instance
- **Environment:** Production config with secrets management

### Database Migrations

**Create Migration:**
```bash
alembic revision --autogenerate -m "Description of changes"
```

**Apply Migrations:**
```bash
alembic upgrade head
```

**Rollback:**
```bash
alembic downgrade -1
```

---

## 4. Development Workflow

### Git Strategy
**Branching Model:** Git Flow (adapted)

**Branch Types:**
- `main` - Production-ready code
- `develop` - Integration branch (optional)
- `feature/*` - New features
- `fix/*` - Bug fixes
- `chore/*` - Maintenance tasks (like this audit)
- `docs/*` - Documentation updates

**Commit Messages:**
Format: `<type>: <description>`

Types:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `chore:` - Maintenance
- `refactor:` - Code refactoring
- `test:` - Test additions/changes
- `style:` - Code style changes
- `perf:` - Performance improvements

**Pull Request Process:**
1. Create feature branch from `main`
2. Make changes and commit
3. Push branch to remote
4. Create PR to `main`
5. Pass CI checks (lint, test, build)
6. Code review
7. Squash and merge

### Code Review Standards
- [ ] Code follows style guidelines
- [ ] Tests are included for new features
- [ ] Documentation is updated
- [ ] No secrets or sensitive data
- [ ] CI passes all checks

---

## 5. Code Quality Standards

### Frontend (JavaScript/TypeScript)

**Linting:** ESLint
- Configuration: `.eslintrc.*`
- Rules: Airbnb or similar standard
- Run: `npm run lint`
- Auto-fix: `npm run lint:fix`

**Formatting:** Prettier
- Configuration: `.prettierrc.*`
- Run: `npm run format`
- Line length: 100
- Semi-colons: Yes
- Single quotes: Yes (configurable)

**Type Checking:** TypeScript
- Strict mode enabled
- Run: `npm run type-check`
- Config: `tsconfig.json`

### Backend (Python)

**Linting:** Ruff
- Fast Python linter
- Configuration: `pyproject.toml` or `ruff.toml`
- Run: `ruff check .`
- Auto-fix: `ruff check . --fix`

**Formatting:** Ruff or Black
- Configuration: `pyproject.toml`
- Run: `ruff format .` or `black .`
- Line length: 100
- String quotes: Double

**Type Checking:** MyPy
- Strict mode recommended
- Run: `mypy src/`
- Config: `pyproject.toml` or `mypy.ini`

**Import Sorting:** isort or Ruff
- Configuration: `pyproject.toml`
- Order: stdlib, third-party, first-party

### Testing

**Frontend:**
- Framework: TBD (Vitest, Jest, or similar)
- Location: `frontend/src/__tests__/` or `*.test.jsx`
- Run: `npm test`

**Backend:**
- Framework: pytest
- Location: `tests/` or inline `test_*.py`
- Run: `pytest`
- Coverage: `pytest --cov=src`

**Coverage Targets:**
- Critical paths: 80%+
- Overall: 70%+

---

## 6. CI/CD Pipeline

### GitHub Actions Workflows
Location: `.github/workflows/`

**Required Workflows:**
1. **Lint & Format Check**
   - Frontend: ESLint + Prettier
   - Backend: Ruff + MyPy
   - Runs on: Every push and PR

2. **Tests**
   - Frontend tests
   - Backend tests (pytest)
   - Coverage reporting
   - Runs on: Every push and PR

3. **Build**
   - Frontend build (Astro)
   - Backend packaging (if applicable)
   - Runs on: Every push and PR

4. **Security Scan**
   - Dependency vulnerabilities (npm audit, pip-audit)
   - Secret scanning (gitleaks)
   - Runs on: Every PR and scheduled

**Deployment Workflows:**
- TBD based on hosting platform

---

## 7. Environment Configuration

### Environment Variables

**Frontend:**
- `PUBLIC_API_URL` - Backend API endpoint
- Other Astro config as needed

**Backend:**
- `DATABASE_URL` - Database connection string
- `SECRET_KEY` - Application secret key
- `DEBUG` - Debug mode (true/false)
- `LOG_LEVEL` - Logging level (DEBUG, INFO, WARNING, ERROR)
- `STORAGE_PATH` - File storage location

**Environment Files:**
- `.env.example` - Template with safe defaults
- `.env` - Local development (not in git)
- `.env.production.template` - Production template

**Secret Management:**
- Development: Local `.env` files
- Production: Environment variables, secret manager, or vault

---

## 8. Dependency Management

### Frontend Dependencies
**File:** `frontend/package.json`

**Update Strategy:**
- Regular updates (monthly or quarterly)
- Security patches: Immediate
- Major versions: Test thoroughly before upgrading

**Audit:**
```bash
npm audit
npm audit fix
```

### Backend Dependencies
**File:** `requirements.txt` or `pyproject.toml`

**Update Strategy:**
- Regular updates (monthly or quarterly)
- Security patches: Immediate
- Pin major versions, allow minor/patch updates

**Audit:**
```bash
pip-audit
# or
safety check
```

### Version Pinning
- **Exact pinning** for production-critical dependencies
- **Caret/tilde ranges** for less critical dependencies
- Document rationale for pinning decisions

---

## 9. Logging & Monitoring

### Logging Standards

**Backend Logging:**
- **Library:** Python `logging` module or `structlog`
- **Format:** JSON structured logs (production) or human-readable (development)
- **Levels:**
  - DEBUG: Detailed diagnostic info
  - INFO: General informational messages
  - WARNING: Warning messages
  - ERROR: Error messages
  - CRITICAL: Critical failures

**Log Destinations:**
- Development: Console
- Production: File + monitoring service (TBD)

### Monitoring (Optional)

**Grafana + Prometheus:**
- Configuration: `config/grafana-monitoring/`
- Docker Compose: `docker-compose.monitoring.yml`
- Metrics: Application metrics, system metrics
- Dashboards: Pre-configured in `config/grafana-monitoring/dashboards/`

---

## 10. Security Conventions

### Secrets Management
- **Never** commit secrets to repository
- Use `.env` files (gitignored)
- Use environment variables in production
- Rotate secrets regularly

### Input Validation
- Validate all user inputs
- Sanitize file uploads
- Use parameterized queries (prevent SQL injection)
- Escape outputs (prevent XSS)

### Authentication & Authorization
- TBD based on requirements
- JWT or session-based auth
- Role-based access control (RBAC) if needed

### Security Headers
- CORS configuration
- CSP (Content Security Policy)
- HTTPS only in production

---

## 11. File Organization Conventions

### Backend Code Structure
```
src/ or backend/
├── api/              # FastAPI routes
├── models/           # Database models
├── schemas/          # Pydantic schemas
├── services/         # Business logic
├── parsers/          # IODD/EDS/PQA parsers
├── storage/          # Storage management
├── utils/            # Utility functions
└── main.py           # Application entry point
```

### Frontend Code Structure
```
frontend/src/
├── components/       # Reusable components
├── content/          # Documentation content (Markdown)
├── layouts/          # Page layouts
├── pages/            # Route pages
├── styles/           # Global styles
└── assets/           # Static assets
```

### Test Data
```
test-data/
├── iodd/             # Sample IODD files
├── eds/              # Sample EDS files
└── fixtures/         # Test fixtures
```

---

## 12. Naming Conventions

### Files & Directories
- **Lowercase with hyphens:** `my-component.jsx`, `user-service.py`
- **Or snake_case for Python:** `user_service.py`, `data_models.py`
- **Directories:** `kebab-case` or `snake_case` consistently

### Code
**JavaScript/TypeScript:**
- **Components:** PascalCase (`MyComponent.jsx`)
- **Functions:** camelCase (`getUserData()`)
- **Constants:** UPPER_SNAKE_CASE (`API_BASE_URL`)
- **Interfaces/Types:** PascalCase (`UserData`)

**Python:**
- **Classes:** PascalCase (`UserService`)
- **Functions:** snake_case (`get_user_data()`)
- **Constants:** UPPER_SNAKE_CASE (`API_BASE_URL`)
- **Private:** Leading underscore (`_private_method()`)

### Git Branches
- `feature/user-authentication`
- `fix/login-bug`
- `chore/repo-audit-2025`
- `docs/api-reference`

---

## 13. Documentation Standards

### Documentation Pages
**Structure:**
- Clear title (H1)
- Table of contents for long pages
- Logical heading hierarchy (H2, H3, H4)
- Code examples with syntax highlighting
- Cross-links to related pages

**Frontmatter (Astro/Starlight):**
```yaml
---
title: Page Title
description: Brief description for SEO and preview
---
```

**Code Blocks:**
````markdown
```python
# Code example with language specified
def example():
    pass
```
````

### Inline Code Comments
- Explain "why" not "what"
- Document complex algorithms
- Include usage examples for public APIs
- No TODO/FIXME without GitHub issue references

---

## 14. Release & Versioning

### Semantic Versioning
Format: `MAJOR.MINOR.PATCH`

- **MAJOR:** Breaking changes
- **MINOR:** New features (backward compatible)
- **PATCH:** Bug fixes (backward compatible)

### Release Process
1. Update `CHANGELOG.md`
2. Create version tag: `git tag v1.2.3`
3. Push tag: `git push origin v1.2.3`
4. Create GitHub Release with notes
5. Deploy to production (manual or automated)

### Changelog Format
Follow [Keep a Changelog](https://keepachangelog.com/) format:
- Added
- Changed
- Deprecated
- Removed
- Fixed
- Security

---

## Summary Checklist

- [x] Documentation path defined: `frontend/src/content/`
- [x] Deprecated paths identified: `docs/`
- [x] Technology stack documented
- [x] Build/deploy flow outlined
- [x] Git workflow defined
- [x] Code quality tools specified
- [x] Environment configuration documented
- [x] Security conventions established
- [x] File organization defined
- [x] Naming conventions standardized

**Status:** Section 1.3 - Complete ✓
