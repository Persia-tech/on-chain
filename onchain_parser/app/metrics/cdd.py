from datetime import date
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import TxOutput


class CDDCalculator:
    def __init__(self, db: Session) -> None:
        self.db = db

    def for_day(self, day: date) -> Decimal:
        age_days = func.extract("epoch", TxOutput.spent_at - TxOutput.created_at) / 86400
        q = (
            select(func.sum((TxOutput.value_sats / 100_000_000.0) * age_days))
            .where(func.date(TxOutput.spent_at) == day)
            .where(TxOutput.spent_at.is_not(None))
        )
        value = self.db.scalar(q)
        return Decimal(value or 0)
