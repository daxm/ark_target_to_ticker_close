#!/usr/bin/env python3

import datetime
import os

import fmpsdk
import matplotlib.dates as mdates
import matplotlib.pylab as plt
import numpy as np
from dotenv import load_dotenv

load_dotenv()


def get_prices_in_target_range(
    start_date: datetime.date,
    end_date: datetime.date,
    symbol: str,
) -> list[dict]:
    historical_prices = fmpsdk.historical_price_full(
        apikey=os.environ.get("API_KEY"),
        symbol=symbol,
    )
    # Sort by date ascending.  (I think it comes out descending.)
    historical_prices.sort(key=lambda e: e["date"])

    prices_in_range = []
    for entry in historical_prices:
        entry_date = datetime.datetime.strptime(entry.get("date"), "%Y-%m-%d").date()
        if start_date <= entry_date <= end_date:
            prices_in_range.append(
                {
                    "date": entry_date,
                    "close": entry.get("close"),
                }
            )
    return prices_in_range


def ark_projections(
    start_date: datetime.date,
    end_date: datetime.date,
    ticker: str,
    expected_price: float,
    bull_price: float,
    bear_price: float,
):
    # Actual related values
    tickers_in_range = get_prices_in_target_range(
        start_date=start_date,
        end_date=end_date,
        symbol=ticker,
    )
    day1_close_price = tickers_in_range[0].get("close")
    day1_date = tickers_in_range[0].get("date")

    # Compute some commonly used values
    range_days_delta = (end_date - start_date).days
    expected_daily_price_delta = (expected_price - day1_close_price) / range_days_delta
    bear_daily_price_delta = (bear_price - day1_close_price) / range_days_delta
    bull_daily_price_delta = (bull_price - day1_close_price) / range_days_delta

    # Build the lists used for graph
    actual_dates = []
    actual_prices = []
    expected_prices = []
    bear_prices = []
    bull_prices = []
    for event in tickers_in_range:
        # Get this entry's day and compute the number of days since the first in the set.
        this_day = event.get("date")
        days_delta = (this_day - day1_date).days

        # Add this day's entries into the datasets.
        actual_dates.append(f"{this_day:%Y-%m-%d}")
        actual_prices.append(event.get("close"))
        expected_prices.append(
            round(
                day1_close_price + days_delta * expected_daily_price_delta,
                2,
            )
        )
        bear_prices.append(
            round(
                day1_close_price + days_delta * bear_daily_price_delta,
                2,
            )
        )
        bull_prices.append(
            round(
                day1_close_price + days_delta * bull_daily_price_delta,
                2,
            )
        )

    plt.plot(
        actual_dates,
        actual_prices,
        color="black",
        label="Actual",
    )
    plt.plot(
        actual_dates,
        expected_prices,
        color="blue",
        label="Expected",
    )
    plt.plot(
        actual_dates,
        bear_prices,
        color="red",
        label="Bear",
    )
    plt.plot(
        actual_dates,
        bull_prices,
        color="green",
        label="Bull",
    )

    min_price = [
        min(actual_prices),
        min(expected_prices),
        min(bull_prices),
        min(bear_prices),
    ]
    max_price = [
        max(actual_prices),
        max(expected_prices),
        max(bull_prices),
        max(bear_prices),
    ]

    price_step = int(os.environ.get("Y_GRAPH_TICKS_STEP"))
    plt.yticks(
        np.arange(
            round(min(min_price) / price_step) * price_step - price_step,
            max(max_price) + price_step,
            price_step,
        )
    )

    date_step = int(os.environ.get("X_GRAPH_TICKS_STEP"))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=date_step))
    plt.gcf().autofmt_xdate()
    plt.xticks(rotation=90)

    plt.legend()
    plt.title(f"Ark {end_date.year} Projections for {ticker.upper()}")

    plt.grid(axis="y")

    plt.show()


if __name__ == "__main__":
    # Environ defaults are ARK's projections for 2027 from 2023.
    ark_projections(
        start_date=datetime.date(
            year=int(os.environ.get("START_YEAR", 2023)),
            month=1,
            day=1,
        ),
        end_date=datetime.date(
            year=int(os.environ.get("END_YEAR", 2027)),
            month=12,
            day=31,
        ),
        expected_price=float(os.environ.get("ARK_EXPECTED_PRICE", 2000)),
        bear_price=float(os.environ.get("ARK_BEAR_PRICE", 1400)),
        bull_price=float(os.environ.get("ARK_BULL_PRICE", 2500)),
        ticker=os.environ.get("TARGET_TICKER"),
    )
