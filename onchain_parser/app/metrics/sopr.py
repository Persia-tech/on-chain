from datetime import date
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import TxOutput


class SOPRCalculator:
    def __init__(self, db: Session) -> None:
        self.db = db

    def for_day(self, day: date) -> Decimal:
        q = (
            select(
                func.sum((TxOutput.value_sats / 100_000_000.0) * TxOutput.spent_price_usd)
                / func.nullif(
                    func.sum((TxOutput.value_sats / 100_000_000.0) * TxOutput.created_price_usd),
                    0,
                )
            )
            .where(func.date(TxOutput.spent_at) == day)
            .where(TxOutput.spent_price_usd.is_not(None))
        )
        value = self.db.scalar(q)
        return Decimal(value or 0)
