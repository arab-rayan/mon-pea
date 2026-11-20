"""Télécharge les cours depuis Yahoo Finance (gratuit, sans clé) et écrit data.json.

Lancé chaque soir de semaine par GitHub Actions (.github/workflows/update-data.yml).
Si un ticker échoue, on garde ses anciennes données au lieu de tout casser.
"""

import json
import os
from datetime import datetime, timezone

import yfinance as yf

START = "2005-01-01"
OUT = os.path.join(os.path.dirname(__file__), "..", "data.json")

TICKERS = {
    "DCAM.PA": {"name": "Amundi PEA Monde MSCI World (DCAM)", "short": "DCAM", "currency": "EUR"},
    "WPEA.PA": {"name": "iShares MSCI World Swap PEA (WPEA)", "short": "WPEA", "currency": "EUR"},
    "CW8.PA": {"name": "Amundi MSCI World (CW8) – historique long", "short": "CW8", "currency": "EUR"},
    "^GSPC": {"name": "S&P 500", "short": "S&P 500", "currency": "USD"},
    "NVDA": {"name": "Nvidia", "short": "Nvidia", "currency": "USD"},
    "EURUSD=X": {"name": "Euro / Dollar", "short": "EUR/USD", "currency": ""},
}


def load_previous():
    try:
        with open(OUT, encoding="utf-8") as f:
            return json.load(f).get("series", {})
    except (OSError, ValueError):
        return {}


def fetch(ticker):
    df = yf.Ticker(ticker).history(start=START, interval="1d", auto_adjust=False)
    df = df[["Close"]].dropna()
    df = df[df["Close"] > 0]
    if df.empty:
        raise ValueError("aucune donnée")
    return {
        "dates": [d.strftime("%Y-%m-%d") for d in df.index],
        "close": [round(float(c), 4) for c in df["Close"]],
    }


def main():
    previous = load_previous()
    series, ok = {}, 0
    for ticker, meta in TICKERS.items():
        try:
            series[ticker] = {**meta, **fetch(ticker)}
            ok += 1
            print(f"OK   {ticker}: {len(series[ticker]['dates'])} cours")
        except Exception as exc:  # noqa: BLE001
            print(f"ERR  {ticker}: {exc}")
            if ticker in previous:
                series[ticker] = previous[ticker]
    if ok == 0:
        raise SystemExit("Aucun cours téléchargé : data.json n'est pas modifié.")
    data = {
        "updated": datetime.now(timezone.utc).isoformat(timespec="minutes"),
        "source": "Yahoo Finance via yfinance",
        "series": series,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
    print(f"data.json écrit ({ok}/{len(TICKERS)} séries à jour)")


if __name__ == "__main__":
    main()
