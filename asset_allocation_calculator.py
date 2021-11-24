import yfinance as yf
import pandas as pd
import numpy as np
import warnings
from empyrical import max_drawdown
from sys import argv, exit


warnings.filterwarnings("ignore")

MONTHS = [f"0{i}" if i < 10 else str(i) for i in range(1, 13)]

MONTHS_NAMES = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Ago",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]


class WrongTickerError(Exception):
    pass


def load(asset, start="2000-01-01"):
    dataset = yf.download(asset, start=start)

    if dataset.shape[0] == 0:
        raise WrongTickerError()

    dataset["date"] = dataset.index.strftime("%Y-%m-%d")

    return dataset


def get_month(data):
    return data["date"].map(lambda v: v.split("-")[1])


def get_year(data):
    return data["date"].map(lambda v: v.split("-")[0])


def add_fields(data):
    data["month"] = get_month(data)
    data["year"] = get_year(data)
    return data


def get_returns(data, base_col="month"):
    data = add_fields(data)

    return pd.DataFrame(
        [
            pd.Series(
                [
                    df_month["Close"]
                    .pct_change(df_month.shape[0] - 1)
                    .tail(1)
                    .values[0]
                    for month, df_month in df_year.groupby(base_col)
                ],
                index=[month for month, df_month in df_year.groupby(base_col)],
            )
            for year, df_year in data.groupby("year")
        ],
        index=[year for year, df_year in data.groupby("year")],
    ).fillna(0)


def drawdown(returns_cum):
    V = [returns_cum.shift(2), returns_cum.shift(1), returns_cum]
    peak, valley, drawdown = 0, 0, 0
    for a, b, c in zip(*V):
        if a <= b and c <= b:
            peak = b
        elif a >= b and c >= b:
            valley = b
        if peak > valley:
            if valley < 0 and peak >= 0:
                valley = -valley
                peak += valley
            elif valley < 0 and peak < 0:
                valley, peak = -peak, -valley

            dd = np.log(valley / peak)

            if dd < drawdown:
                drawdown = dd

    return drawdown


def evaluate_returns(data):
    returns, N, P = data
    r_counts = returns[returns != 0]
    returns_norm = returns.replace([np.nan, np.inf, -np.inf], 0)
    acc_counts = (r_counts > 0).value_counts(normalize=True)
    mean_profit = returns[returns > 0].mean()
    mean_loss = -returns[returns <= 0].mean()
    std_loss = -returns[returns <= 0].std()
    em = 100 * (
        (mean_profit * acc_counts.get(True, 0)) - (mean_loss * acc_counts.get(False, 0))
    )
    payoff = mean_profit / mean_loss
    max_profit = returns[returns > 0].max()
    max_loss = -returns[returns < 0].min()
    acc = acc_counts.get(True, 0)
    sharpe = returns_norm.mean() / returns_norm.std()
    returns_cumulative = returns.fillna(0).cumsum()

    return pd.Series(
        {
            "#trades": N,
            "#trades_year": N / 3,
            "#trades_month": N / (3 * 12),
            "%trades": P * 100,
            "em": em,
            "acc(%)": acc * 100,
            "payoff": payoff,
            "kelly(%)": (acc - ((1 - acc) / payoff)) * 100,
            "max_profit(%)": max_profit * 100,
            "max_loss(%)": max_loss * 100,
            "mean_profit(%)": mean_profit * 100,
            "mean_loss(%)": mean_loss * 100,
            "std_loss(%)": std_loss * 100,
            "total_return(%)": returns_cumulative.values[-1] * 100
            if returns_cumulative.shape[0] > 0
            else 0,
            "max_drawdown(%)": max_drawdown(returns) * 100,
            "ina_drawdown(%)": drawdown(returns_cumulative) * 100,
            "bottom_line(%)": returns_cumulative.min() * 100,
            "sharpe": returns.mean() / returns.std(),
        }
    )


def backtest(data, base_col="month", ref_cols=MONTHS):
    default_series = pd.Series(np.zeros(20,))

    return pd.DataFrame(
        [
            evaluate_returns(((get_returns(data, base_col=base_col)).get(col, default_series), 12, 1))
            for col in ref_cols
        ],
        index=ref_cols,
    )


def define_percentages(data, percentage):
    data_backtest = backtest(data, base_col="month", ref_cols=MONTHS)

    max_acceptable_drawdown = (-data_backtest["max_drawdown(%)"]).mean()

    em_negative = ~(data_backtest["em"] < 0)
    drawdown_under_acceptable_levels = (
        -data_backtest["max_drawdown(%)"]
    ) < max_acceptable_drawdown

    return np.round(
        percentage
        * ((data_backtest["kelly(%)"] // 2) / 100)
        * (em_negative * drawdown_under_acceptable_levels)
    )


def pipeline(asset, percentage):
    try:
        dataset = load(asset)
    except WrongTickerError:
        error_message = f"ERROR: Failed to download {asset}. "
        error_message += "Verify if it is a valid Yahoo Finance ticker"
        print(error_message)
        exit(1)
    defined_percentages = define_percentages(dataset, percentage)
    return pd.Series(defined_percentages, name=asset)


def retrieve_assets_and_percentages(args):
    assets = []
    percentages = []

    add_perc = False

    for input_ in args:
        if add_perc:
            try:
                percentages.append(int(input_))
            except ValueError:
                print("ERROR: Percentages must be natural numbers between 1 and 100")
                exit(1)
        elif input_ != "--perc":
            assets.append(input_)
        else:
            add_perc = True

    if len(percentages) == 0:
        percentages = np.repeat(100 / len(assets), len(assets))

    return assets, percentages


def main(args):
    assets, percentages = retrieve_assets_and_percentages(args)
    results = [
        pipeline(asset, percentage)
        for asset, percentage in zip(assets, percentages)
    ]

    summary = pd.DataFrame(results).replace(-0, 0)
    summary.columns = MONTHS_NAMES
    summary = summary.transpose()
    summary["Fixed Income"] = 100 - summary.sum(axis=1)
    print(summary)


if __name__ == "__main__":
    main(argv[1:])
