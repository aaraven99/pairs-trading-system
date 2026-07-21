from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class PaperOrder:
    symbol: str
    qty: float
    side: str
    type: str = "market"
    time_in_force: str = "day"


class AlpacaPaperAdapter:
    """Deliberately dry-run by default; no live endpoint is accepted."""

    def __init__(self, dry_run: bool = True) -> None:
        self.dry_run = dry_run
        self.base_url = os.getenv("ALPACA_BASE_URL", "https://paper-api.alpaca.markets")
        if "paper" not in self.base_url:
            raise ValueError("only Alpaca paper endpoints are permitted")

    def payload(self, order: PaperOrder) -> dict[str, str]:
        if order.side not in {"buy", "sell"} or order.qty <= 0:
            raise ValueError("order side and positive quantity are required")
        return {
            "symbol": order.symbol.upper(),
            "qty": str(order.qty),
            "side": order.side,
            "type": order.type,
            "time_in_force": order.time_in_force,
        }

    def submit(self, order: PaperOrder) -> dict[str, object]:
        return {"dry_run": self.dry_run, "endpoint": self.base_url, "order": self.payload(order)}
