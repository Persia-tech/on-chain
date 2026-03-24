from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.bitcoin.prices import PriceClient
from app.models import Block, TxOutput


class BlockParser:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.price_client = PriceClient()

    def parse_block(self, block: dict, height: int) -> None:
        timestamp = datetime.fromtimestamp(block["time"], tz=timezone.utc)
        block_row = Block(height=height, hash=block["hash"], timestamp=timestamp)
        self.db.merge(block_row)

        usd_price = self.price_client.get_btc_usd_price(timestamp)

        for tx in block.get("tx", []):
            txid = tx["txid"]
            for vout in tx.get("vout", []):
                value_sats = int(float(vout.get("value", 0)) * 100_000_000)
                if value_sats <= 0:
                    continue
                txo = TxOutput(
                    txid=txid,
                    vout=int(vout["n"]),
                    block_height=height,
                    value_sats=value_sats,
                    created_at=timestamp,
                    created_price_usd=usd_price,
                )
                self.db.merge(txo)

            for vin in tx.get("vin", []):
                prev_txid = vin.get("txid")
                prev_vout = vin.get("vout")
                if prev_txid is None or prev_vout is None:
                    continue
                prev_output = self.db.get(TxOutput, {"txid": prev_txid, "vout": prev_vout})
                if prev_output is None:
                    continue
                prev_output.spent_in_txid = txid
                prev_output.spent_at = timestamp
                prev_output.spent_price_usd = usd_price
