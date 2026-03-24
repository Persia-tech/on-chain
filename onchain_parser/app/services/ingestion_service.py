from sqlalchemy.orm import Session

from app.bitcoin.sync import BlockchainSync


class IngestionService:
    def __init__(self, db: Session) -> None:
        self.syncer = BlockchainSync(db)

    def sync_once(self, start_height: int | None = None, end_height: int | None = None) -> int:
        return self.syncer.sync(start_height=start_height, end_height=end_height)
