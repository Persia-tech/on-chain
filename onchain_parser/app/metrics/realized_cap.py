from datetime import date
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import TxOutput


class RealizedCapCalculator:
    def __init__(self, db: Session) -> None:
        self.db = db

    def for_day(self, day: date) -> Decimal:
        q = (
            select(func.sum((TxOutput.value_sats / 100_000_000.0) * TxOutput.created_price_usd))
            .where(func.date(TxOutput.created_at) <= day)
            .where(TxOutput.spent_at.is_(None))
        )
        value = self.db.scalar(q)
        return Decimal(value or 0)
