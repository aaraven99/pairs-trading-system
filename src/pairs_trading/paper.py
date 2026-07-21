from __future__ import annotations

import os
import json
from dataclasses import dataclass
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class PaperOrder:
    symbol: str
    qty: float
    side: str
    type: str = "market"
    time_in_force: str = "day"


class AlpacaPaperAdapter:
    """Paper-only broker adapter; dry run remains the default."""

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
        payload = self.payload(order)
        if self.dry_run:
            return {"dry_run": True, "endpoint": self.base_url, "order": payload}
        key, secret = os.getenv("ALPACA_API_KEY"), os.getenv("ALPACA_SECRET_KEY")
        if not key or not secret:
            raise RuntimeError("ALPACA_API_KEY and ALPACA_SECRET_KEY are required for paper submission")
        request = Request(
            f"{self.base_url}/v2/orders",
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json", "APCA-API-KEY-ID": key, "APCA-API-SECRET-KEY": secret},
            method="POST",
        )
        with urlopen(request, timeout=15) as response:  # nosec B310: validated paper endpoint
            return {"dry_run": False, "order": json.load(response)}
