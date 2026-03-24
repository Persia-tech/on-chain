from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas import HealthResponse, MetricPoint
from app.services.metric_service import MetricService

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@router.get("/metrics/daily", response_model=list[MetricPoint])
def get_daily_metrics(limit: int = 30, db: Session = Depends(get_db)) -> list[MetricPoint]:
    service = MetricService(db)
    return service.latest(limit=limit)
