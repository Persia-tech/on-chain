from decimal import Decimal


def compute_nupl(market_cap_usd: Decimal, realized_cap_usd: Decimal) -> Decimal:
    if market_cap_usd == 0:
        return Decimal(0)
    return (market_cap_usd - realized_cap_usd) / market_cap_usd
