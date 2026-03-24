from app.db import SessionLocal
from app.services.ingestion_service import IngestionService


if __name__ == "__main__":
    with SessionLocal() as db:
        service = IngestionService(db)
        parsed = service.sync_once()
        print(f"Parsed {parsed} blocks")
