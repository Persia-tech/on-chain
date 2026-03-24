# PowerPoint Draft (Non-Technical)

Use the following as ready-to-copy slide content for a non-technical audience.

---

## Slide 1 — Title
**Bitcoin On-Chain Intelligence Engine (MVP)**

**Subtitle:** Turning raw blockchain data into simple daily market signals.

---

## Slide 2 — The Problem
- Bitcoin blockchain data is huge and hard to interpret.
- Most people see noise, not clear insight.
- Teams need one trusted pipeline for daily decision metrics.

**Speaker note:** “We are building the data foundation first, not a flashy app first.”

---

## Slide 3 — Our Solution (Simple View)
- Connect to Bitcoin node data.
- Organize every coin movement in a structured database.
- Compute key indicators each day:
  - Realized Cap
  - MVRV
  - NUPL
  - SOPR
  - CDD
- Feed results to dashboards and alerts.

---

## Slide 4 — What This MVP Delivers
- Reliable block-by-block ingestion.
- Historical + incremental updates.
- Daily metric computation service.
- API for dashboard integration.

**Outcome:** A reusable analytics engine, not a one-off script.

---

## Slide 5 — Business Value
- Faster market-cycle visibility.
- Consistent metric definitions across team.
- Less manual data wrangling.
- Foundation to launch products faster (dashboard, alerts, research reports).

---

## Slide 6 — 3-Phase Roadmap
### Phase 1 (Now): Correct MVP
- Accurate parser + core metrics.

### Phase 2: Performance
- Chunking, indexing, caching, daily incremental jobs.

### Phase 3: Advanced Intelligence
- Age bands, LTH/STH approximations, miner heuristics, clustering.

---

## Slide 7 — Risks and Mitigation
- **Risk:** Large data volume.
  - **Mitigation:** Incremental updates + indexed tables.
- **Risk:** Data/provider inconsistencies.
  - **Mitigation:** Validation checks + retryable jobs.
- **Risk:** Scope creep.
  - **Mitigation:** Keep MVP focused on top 5 metrics.

---

## Slide 8 — What We Need Next
- Stable Bitcoin Core node access.
- Production Postgres instance.
- One trusted market-cap/price source.
- 1–2 weeks for hardening and first dashboard integration.

**Closing line:** “We now have the engine blueprint to convert blockchain complexity into actionable signals.”
