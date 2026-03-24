from datetime import datetime, timezone

import httpx

from app.config import get_settings


class PriceClient:
    def __init__(self) -> None:
        self._base_url = get_settings().price_api_url

    def get_btc_usd_price(self, timestamp: datetime) -> float:
        day = timestamp.astimezone(timezone.utc).strftime("%d-%m-%Y")
        url = f"{self._base_url}/coins/bitcoin/history"
        params = {"date": day, "localization": "false"}
        response = httpx.get(url, params=params, timeout=20)
        response.raise_for_status()
        data = response.json()
        return float(data["market_data"]["current_price"]["usd"])
