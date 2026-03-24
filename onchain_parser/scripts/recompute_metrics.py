from datetime import date
from decimal import Decimal

from app.db import SessionLocal
from app.services.metric_service import MetricService


if __name__ == "__main__":
    with SessionLocal() as db:
        service = MetricService(db)
        # Placeholder market cap value; replace with trusted market cap feed.
        row = service.upsert_daily(day=date.today(), market_cap_usd=Decimal("0"))
        print(f"Upserted metrics for {row.day}")
