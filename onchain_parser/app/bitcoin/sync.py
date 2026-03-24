from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.bitcoin.parser import BlockParser
from app.bitcoin.rpc import get_rpc_client
from app.models import Block


class BlockchainSync:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.parser = BlockParser(db)
        self.rpc = get_rpc_client()

    def sync(self, start_height: int | None = None, end_height: int | None = None) -> int:
        if start_height is None:
            latest_synced = self.db.scalar(select(func.max(Block.height)))
            start_height = 0 if latest_synced is None else latest_synced + 1

        chain_height = self.rpc.getblockcount()
        target_height = chain_height if end_height is None else min(end_height, chain_height)

        parsed = 0
        for height in range(start_height, target_height + 1):
            block_hash = self.rpc.getblockhash(height)
            block = self.rpc.getblock(block_hash, 2)
            self.parser.parse_block(block=block, height=height)
            parsed += 1

            if parsed % 50 == 0:
                self.db.commit()

        self.db.commit()
        return parsed
