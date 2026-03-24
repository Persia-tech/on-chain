from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import BigInteger, Date, DateTime, ForeignKey, Index, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class Block(Base):
    __tablename__ = "blocks"

    height: Mapped[int] = mapped_column(Integer, primary_key=True)
    hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)


class TxOutput(Base):
    __tablename__ = "tx_outputs"

    txid: Mapped[str] = mapped_column(String(64), primary_key=True)
    vout: Mapped[int] = mapped_column(Integer, primary_key=True)
    block_height: Mapped[int] = mapped_column(ForeignKey("blocks.height"), index=True)
    value_sats: Mapped[int] = mapped_column(BigInteger)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    created_price_usd: Mapped[Decimal] = mapped_column(Numeric(20, 4), default=0)
    spent_in_txid: Mapped[str | None] = mapped_column(String(64), nullable=True)
    spent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    spent_price_usd: Mapped[Decimal | None] = mapped_column(Numeric(20, 4), nullable=True)


class DailyMetric(Base):
    __tablename__ = "daily_metrics"

    day: Mapped[date] = mapped_column(Date, primary_key=True)
    realized_cap_usd: Mapped[Decimal] = mapped_column(Numeric(24, 2), default=0)
    market_cap_usd: Mapped[Decimal] = mapped_column(Numeric(24, 2), default=0)
    mvrv: Mapped[Decimal] = mapped_column(Numeric(20, 8), default=0)
    nupl: Mapped[Decimal] = mapped_column(Numeric(20, 8), default=0)
    sopr: Mapped[Decimal] = mapped_column(Numeric(20, 8), default=0)
    cdd: Mapped[Decimal] = mapped_column(Numeric(24, 8), default=0)


Index("ix_tx_outputs_unspent", TxOutput.spent_at, TxOutput.block_height)
