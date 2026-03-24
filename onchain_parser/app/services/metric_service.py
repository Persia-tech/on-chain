from datetime import date
from decimal import Decimal

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.metrics.cdd import CDDCalculator
from app.metrics.mvrv import compute_mvrv
from app.metrics.nupl import compute_nupl
from app.metrics.realized_cap import RealizedCapCalculator
from app.metrics.sopr import SOPRCalculator
from app.models import DailyMetric
from app.schemas import MetricPoint


class MetricService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.realized = RealizedCapCalculator(db)
        self.sopr = SOPRCalculator(db)
        self.cdd = CDDCalculator(db)

    def upsert_daily(self, day: date, market_cap_usd: Decimal) -> DailyMetric:
        realized_cap = self.realized.for_day(day)
        row = self.db.get(DailyMetric, day) or DailyMetric(day=day)
        row.realized_cap_usd = realized_cap
        row.market_cap_usd = market_cap_usd
        row.mvrv = compute_mvrv(market_cap_usd=market_cap_usd, realized_cap_usd=realized_cap)
        row.nupl = compute_nupl(market_cap_usd=market_cap_usd, realized_cap_usd=realized_cap)
        row.sopr = self.sopr.for_day(day)
        row.cdd = self.cdd.for_day(day)
        self.db.merge(row)
        self.db.commit()
        return row

    def latest(self, limit: int = 30) -> list[MetricPoint]:
        q = select(DailyMetric).order_by(desc(DailyMetric.day)).limit(limit)
        rows = list(self.db.scalars(q))
        return [MetricPoint.model_validate(row, from_attributes=True) for row in rows]
