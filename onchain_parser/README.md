# onchain_parser

Python-first project skeleton for full Bitcoin blockchain parsing and on-chain analytics.

## MVP Scope

- Block-by-block parsing from Bitcoin Core RPC
- UTXO + spend tracking in Postgres
- Daily realized cap
- MVRV / NUPL / SOPR / CDD computation pipeline
- Lightweight API for dashboard integration

## Quick Start

1. Copy env and update values:
   ```bash
   cp .env.example .env
   ```
2. Install dependencies:
   ```bash
   pip install -e .
   ```
3. Initialize database:
   ```bash
   python scripts/init_db.py
   ```
4. Sync blockchain data once:
   ```bash
   python scripts/sync_once.py
   ```
5. Recompute metrics:
   ```bash
   python scripts/recompute_metrics.py
   ```
6. Run API:
   ```bash
   uvicorn app.main:app --reload
   ```

## Roadmap

- Phase 1: Correctness-first parser and baseline metrics
- Phase 2: Chunked processing, indexes, caching, daily incremental sync
- Phase 3: Age bands, LTH/STH, miner heuristics, entity clustering
