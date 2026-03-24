# On-Chain Intelligence Dashboard + Telegram Bot (MVP Blueprint)

## 0) Reasonable assumptions (so we can move fast)
- **Network focus for v1:** Bitcoin only.
- **Data cadence for v1:** daily close values (not intraday ticks).
- **User type:** crypto trader/researcher who wants signal summaries instead of raw chain noise.
- **Delivery:** web dashboard + Telegram alerts for threshold events.

---

## 1) Clarify the idea

### Product definition
Build a web dashboard and Telegram bot that aggregates the most decision-useful on-chain metric families into a single, consistent analytics layer with alerts.

### Core problem solved
On-chain data is fragmented across tools and often lacks consistent definitions. Traders/researchers waste time gathering, normalizing, and monitoring metrics.

### Target user + use case
- **Primary user:** discretionary crypto trader, quant researcher, crypto PM.
- **Use case:** quickly assess cycle risk (overheated vs undervalued), flow pressure (miners/exchanges), and holder behavior (whales/age cohorts), then get alerted when conditions change.

---

## 2) Define the MVP (smallest usable product)

### Essential features only
1. **Dashboard tabs for metric families:**
   - MVRV Family
   - Realized Value
   - Profit & Loss
   - Spending Behavior
   - Miner Supply Pressure
   - Supply Distribution
   - Liquidity & Exchange
   - Whale / Large Holder
   - Coin Age / Lifecycle
2. **Unified timeseries viewer** (date range + metric selector).
3. **Signal cards** (simple rule-based states: Bullish / Neutral / Bearish).
4. **Telegram bot alerts** for threshold crossings (e.g., MVRV Z > X, exchange inflow spike).
5. **Daily ETL pipeline** that ingests, validates, stores, and serves metrics.

### Explicitly out of scope for MVP
- Multi-chain support.
- AI forecasting.
- Complex backtesting UI.
- User billing and team workspaces.

---

## 3) System design (minimal but extensible)

## High-level architecture
1. **Ingestion worker** pulls on-chain data from provider APIs daily.
2. **Metric engine** standardizes formulas and computes derived fields.
3. **Timeseries DB** stores raw + normalized + derived metrics.
4. **Backend API** serves dashboard + bot + signal endpoints.
5. **Frontend app** renders charts, cards, and metric-family pages.
6. **Telegram bot service** subscribes to alert rules and pushes updates.

## Components

### Frontend
- Next.js app with:
  - `Overview` page (regime snapshot)
  - `Metric Family` pages (shared chart component)
  - `Alerts` page (configure thresholds)

### Backend
- FastAPI service:
  - `/metrics` (query normalized series)
  - `/signals` (current regime states)
  - `/alerts` (CRUD thresholds)
  - `/health` (service checks)

### Database
- PostgreSQL + TimescaleDB extension.
- Tables:
  - `raw_observations`
  - `normalized_metrics`
  - `derived_metrics`
  - `signal_states`
  - `user_alert_rules`
  - `alert_events`

### External APIs (replaceable adapters)
- Primary market + on-chain source (e.g., Glassnode, CryptoQuant, CoinMetrics).
- Price feed for denominated ratios (if not in provider response).
- Telegram Bot API.

---

## 4) Recommended stack

### Why this stack
- Fast to build.
- Common and maintainable.
- Scales from solo project to small team.

### Stack choice
- **Frontend:** Next.js + TypeScript + Tailwind + Recharts.
- **Backend:** FastAPI + Pydantic + SQLAlchemy.
- **Jobs:** APScheduler (MVP) or Celery (when load grows).
- **DB:** PostgreSQL + TimescaleDB.
- **Cache/queue (optional in MVP):** Redis.
- **Infra:** Docker Compose (dev), single VM/container deploy first.
- **Monitoring:** Prometheus + Grafana + Sentry (start light).

---

## 5) Step-by-step execution plan

### Step 1: Setup (day 1-2)
- Initialize monorepo:
  - `apps/web`
  - `apps/api`
  - `services/bot`
  - `services/ingestion`
  - `packages/shared`
- Add Docker Compose (postgres + timescaledb + api + web).
- Add base CI (lint + tests + build).

### Step 2: Data model + ingestion (day 3-5)
- Implement provider adapter interface.
- Create `raw_observations` and `normalized_metrics` pipeline.
- Add daily ingestion job with idempotent upserts.

### Step 3: Core API + dashboard (day 6-9)
- Build `/metrics` and `/signals` endpoints.
- Build dashboard with shared timeseries chart + family tabs.
- Add regime card logic (simple threshold rules).

### Step 4: Telegram alerts (day 10-11)
- Build alert rule CRUD.
- Build bot commands (`/start`, `/alerts`, `/set`).
- Run evaluator job daily (or hourly) and send notifications.

### Step 5: Polish + reliability (day 12-14)
- Add input validation + data quality checks.
- Add retries + dead-letter logging for failed pulls.
- Add basic observability dashboards.

---

## 6) Code package (starter implementation outline for Codex)

## Suggested repository structure
```text
onchain-intel/
  apps/
    web/
    api/
  services/
    ingestion/
    bot/
  packages/
    shared/
  infra/
    docker-compose.yml
```

## Shared metric catalog schema
```json
{
  "metric_id": "mvrv_zscore",
  "family": "mvrv",
  "display_name": "MVRV Z-Score",
  "unit": "ratio",
  "frequency": "1d",
  "source": "glassnode",
  "higher_is": "risk_on",
  "default_thresholds": {
    "bullish": 0.5,
    "bearish": 6.0
  }
}
```

## API contract (minimal)
- `GET /v1/metrics?metric_id=mvrv_zscore&start=2023-01-01&end=2026-01-01`
- `GET /v1/signals/current`
- `POST /v1/alerts`
- `GET /v1/alerts`
- `DELETE /v1/alerts/{id}`

## Core backend modules
- `adapters/` (one file per provider)
- `metrics/transformers.py` (normalize + derived formulas)
- `signals/rules.py` (regime logic)
- `alerts/evaluator.py` (threshold engine)
- `api/routes/*.py`

## Telegram bot commands
- `/start` register user
- `/help` list commands
- `/alerts` list active rules
- `/set mvrv_zscore > 5.8` create rule
- `/del 23` remove rule

## Data quality checks
- reject non-monotonic dates
- reject missing values above threshold
- reject metric jumps above configurable z-score unless source confirms revision

---

## 7) Iterate like a builder (after v1 ships)

### Immediate improvements
1. Add **cross-metric composite index** (cycle heat score).
2. Add **scenario tags** (Capitulation, Euphoria, Distribution).
3. Add **watchlists** (user picks 5-10 key metrics).
4. Add **weekly summary Telegram digest**.

### Bottlenecks to watch
- API provider rate limits.
- Schema drift from providers.
- Alert spam from noisy metrics.

### Next best feature
Add **signal explainability**: every alert should include why it fired, last 30-day context, and percentile rank.

---

## 8) Startup execution mindset
- Ship in 2 weeks with daily data first.
- Validate usefulness through alert retention and dashboard revisit rate.
- Only add complexity when there is repeated user demand.
- Keep formulas and thresholds transparent to build trust.

