from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str


class MetricPoint(BaseModel):
    day: date
    realized_cap_usd: Decimal
    market_cap_usd: Decimal
    mvrv: Decimal
    nupl: Decimal
    sopr: Decimal
    cdd: Decimal
