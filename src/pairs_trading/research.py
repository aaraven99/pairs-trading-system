from __future__ import annotations

import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import coint


def hedge_ratio(y: pd.Series, x: pd.Series) -> float:
    aligned = pd.concat([y, x], axis=1).dropna()
    if len(aligned) < 3:
        raise ValueError("at least three aligned observations are required")
    return float(
        np.linalg.lstsq(
            np.c_[np.ones(len(aligned)), aligned.iloc[:, 1]], aligned.iloc[:, 0], rcond=None
        )[0][1]
    )


def spread_zscore(y: pd.Series, x: pd.Series, lookback: int = 20) -> pd.Series:
    spread = y - hedge_ratio(y, x) * x
    mean, std = spread.rolling(lookback).mean(), spread.rolling(lookback).std(ddof=0)
    return spread.sub(mean).div(std.replace(0, np.nan))


def screen_pair(y: pd.Series, x: pd.Series) -> dict[str, float]:
    stat, pvalue, _ = coint(y.dropna(), x.dropna())
    return {
        "cointegration_stat": float(stat),
        "pvalue": float(pvalue),
        "hedge_ratio": hedge_ratio(y, x),
    }


def zscore_signals(
    zscore: pd.Series, entry: float = 2.0, exit: float = 0.5, stop: float = 3.5
) -> pd.Series:
    position = 0
    signals: list[int] = []
    for value in zscore.fillna(0):
        if abs(value) >= stop:
            position = 0
        elif position == 0 and value >= entry:
            position = -1
        elif position == 0 and value <= -entry:
            position = 1
        elif position and abs(value) <= exit:
            position = 0
        signals.append(position)
    return pd.Series(signals, index=zscore.index, name="spread_position")
