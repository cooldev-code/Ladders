# Ladders Job Ingestion and Search System

A take-home implementation that ingests heterogeneous job JSON feeds, applies publication approval rules, stores approved jobs, and exposes a searchable UI.

## Architecture

```text
JSON feeds -> Ingestion/Normalizer -> Approval Engine -> Approved Repository
                                                    -> Rejection Logger
Approved Repository -> FastAPI -> React search UI
```

The backend is organized into focused modules:

- `app/models/` — canonical job domain models
- `app/domain/` — shared location and salary helpers used by rules, storage, and API
- `app/ingestion/` — feed reading and normalization for multiple JSON shapes
- `app/approval/` — pluggable rules evaluated by `ApprovalEngine`
- `app/storage/` — in-memory approved job store, rejection log, and query service
- `app/pipeline.py` — orchestrates ingest → approve → persist
- `app/api/routes/` — REST endpoints split into `jobs.py` and `admin.py`

## Approval rules

Jobs are approved only when **all** rules pass:

1. Title is non-empty
2. Remote anywhere **or** in-person in US/Canada
3. Full-time employment
4. Salary above `$100,000 USD` annual **or** `$45 USD` hourly (after currency normalization)
5. Not from a staffing firm
6. English language, or French when located in Canada

Rejected jobs are logged to `data/rejected_jobs.jsonl` with all failure reasons.

## Sample data results

Running the pipeline against `data/feeds/feed_a.json` (20 jobs, two JSON formats):

- **11 approved**
- **9 rejected**
- **0 ingestion errors**

Approved titles:

- Backend Engineer
- Machine Learning Engineer
- Agile Project Lead
- Senior Software Engineer
- Data Scientist
- QA Automation Engineer
- UX Designer
- Product Analyst
- Cybersecurity Specialist
- Growth Marketing Manager
- Customer Success Manager

## Assumptions

1. **Currency conversion** uses static mock rates in `backend/app/config.py` (`USD`, `CAD`, `GBP`, `EUR`).
2. **Hourly detection** uses explicit `unit: "hourly"` or bare numeric salaries `<= 500`.
3. **Location parsing** is intentionally simple: comma-split strings and direct country field matching.
4. **Consulting agencies** are allowed; only staffing firms are rejected.
5. **Both feeds** refers to structured vs flat/scraped JSON shapes within the sample file.

## Prerequisites

- Python 3.10+
- Node.js 18+

## Backend setup

```bash
cd backend
pip install -r requirements.txt
set PYTHONPATH=.
python -m uvicorn app.main:app --reload
```

API runs at `http://127.0.0.1:8000`.

### Useful endpoints

- `GET /api/health`
- `GET /api/jobs?q=engineer&country=Canada&sort_by=salary&order=desc&page=1&page_size=5`
  returns a paginated envelope: `{ items, total, page, page_size, total_pages, has_next, has_prev }`
- `GET /api/stats` headline catalog stats (`total`, `remote`, `countries`)
- `GET /api/jobs/{id}`
- `GET /api/admin/rejected`
- `POST /api/admin/ingest`

### Run tests

```bash
cd backend
set PYTHONPATH=.
python -m pytest tests -v
python -m pytest tests/test_requirements.py -v
```

## Frontend setup

Built with **React**, **TypeScript**, **Vite**, **Tailwind CSS v4**, and **[shadcn/ui](https://ui.shadcn.com/)**.

```bash
cd frontend
npm install
npm run dev
```

UI runs at `http://localhost:5173` and proxies `/api` to the backend.

shadcn/ui components live under `frontend/src/components/ui/`. Add more with:

```bash
npx shadcn@latest add button
```

## Adding a new approval rule

1. Create a class in `backend/app/approval/rules/` implementing `evaluate(job) -> RuleResult`.
2. Register it in `default_rules()` inside `backend/app/approval/__init__.py`.
3. Add unit tests under `backend/tests/test_rules/`.

Example future rule: approve remote UK jobs with `>= 90k USD` by adding a dedicated `LocationSalaryRule` without changing existing rule classes.

## Project layout

```text
Ladders/
  backend/
    app/
      domain/
      models/
      ingestion/
      approval/
      storage/
      api/routes/
    tests/
  frontend/
    components.json
    src/
      components/
        ui/
      lib/
      api/
      hooks/
      types/
      utils/
  data/feeds/feed_a.json
  README.md
```
