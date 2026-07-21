import argparse
import json

import yfinance as yf

from .research import screen_pair, spread_zscore, zscore_signals


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--left", default="KO")
    parser.add_argument("--right", default="PEP")
    parser.add_argument("--start", default="2022-01-01")
    args = parser.parse_args()
    data = yf.download([args.left, args.right], start=args.start, auto_adjust=True, progress=False)[
        "Close"
    ]
    stats = screen_pair(data[args.left], data[args.right])
    signals = zscore_signals(spread_zscore(data[args.left], data[args.right]))
    print(json.dumps({**stats, "active_position": int(signals.iloc[-1])}, indent=2))
