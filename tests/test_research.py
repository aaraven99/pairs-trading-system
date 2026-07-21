import numpy as np
import pandas as pd
import pytest

from pairs_trading.paper import AlpacaPaperAdapter, PaperOrder
from pairs_trading.research import hedge_ratio, zscore_signals


def test_hedge_ratio_and_signal_exits() -> None:
    x = pd.Series(np.arange(1, 30, dtype=float))
    assert hedge_ratio(2 * x + 1, x) == pytest.approx(2)
    assert zscore_signals(pd.Series([0, 2.1, 0.2, -2.2])).tolist() == [0, -1, 0, 1]


def test_paper_adapter_is_safe(monkeypatch: pytest.MonkeyPatch) -> None:
    adapter = AlpacaPaperAdapter()
    assert adapter.submit(PaperOrder("spy", 3, "buy"))["dry_run"]
    monkeypatch.setenv("ALPACA_BASE_URL", "https://api.alpaca.markets")
    with pytest.raises(ValueError):
        AlpacaPaperAdapter()
