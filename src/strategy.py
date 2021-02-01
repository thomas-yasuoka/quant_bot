import pandas as pd
# from passwords import *
from pandas_datareader import data
import datetime
from calendar import monthrange
import time

def get_monthly_rets(tick_pickle="../data/ibovespa_tickers.zip"):
    """
    Devolve os retornos mensais, além de exportá-los
    (junto dos respectivos tickers) pra returns_last_month.zip (pickle)
    """
    tickers = pd.read_pickle(tick_pickle)
    tickers = tickers + ".SAO"

    months = [12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    last_month = datetime.date.today().replace(day=1) - datetime.timedelta(days=1)
    year = last_month.year
    month = last_month.month
    days_month = monthrange(year, month)[1]

    errors = []
    rets = {}
    count = 0

    print(last_month)
    print(datetime.datetime(last_month.year, last_month.month, monthrange(last_month.year, last_month.month)[1]).date())

    for i in tickers:
        if count % 5 != 0 or count == 0:
            try:
                complete = data.DataReader(i,
                                            "av-daily-adjusted",
                                            start=last_month.replace(day=1),
                                            end=datetime.datetime(last_month.year, last_month.month, monthrange(last_month.year, last_month.month)[1]).date()
                                            )
                rets[i] = complete["adjusted close"][-1]/complete["adjusted close"][0]
            except Exception as e:
                errors.append(i)
                print(f"ERROR IN {i}: {e}")
            count += 1
        else:
            time.sleep(60)
            count += 1
    
    rets = pd.DataFrame(rets, index=[0])
    rets.to_pickle("../data/returns_last_month.zip")
    return rets

def strat(best_pickle="../data/returns_last_month.zip"):
    """
    Pega um pickle com os retornos mensais e escolhe os 10 melhores
    o nome está genérico para mostrar na reunião e ñ dar spoiler pros membros novos
    """
    df = pd.read_pickle(best_pickle)
    lst = df.sort_values(0, axis=1, ascending=False).iloc[0, :10].index.str[:-4] + "F"

    return list(lst)

def vwap(symbol="PETR4F"):
    """
    fix decimal error things
    take today's data
    make code prettier
    auto-delete image, or make ../img folder
    """
    # datetime.now(tz=pytz.UTC)
    # datetime.utcnow()
    ticks = mt5.copy_ticks_range(
            "PETR4F",
            datetime.datetime(2021, 1, 5, 10, 2, tzinfo=pytz.UTC),
            datetime.datetime(2021, 1, 5, 18, tzinfo=pytz.UTC), 
            mt5.COPY_TICKS_TRADE
            )
    ticks = pd.DataFrame(ticks)
    ticks["time"] = pd.to_datetime(ticks["time"], unit="s")
    ticks["Symbol"] = symbol 
    ticks.index = ticks["time"]
    
    grouped = ticks.groupby("Symbol")

    ask = grouped["ask"].resample("1Min").ohlc()

    vol = grouped["volume"].resample("1Min").sum()
    ask_wv = pd.concat([ask, vol], axis=1)
    ask_wv["tpv"] = (ask_wv["high"] + ask_wv["low"] + ask_wv["close"]) / 3 * ask_wv["volume"]
    ask = ask.reset_index()

    ask_wv["cumulative_vol"] = ask_wv["volume"].cumsum()
    ask_wv["cumulative_tpv"] =  ask_wv["tpv"].cumsum()
    ask_wv["vwap"] = ask_wv["cumulative_tpv"] / ask_wv["cumulative_vol"]

    ask_wv = ask_wv.reset_index()
    ask_wv.index = ask_wv["time"]
    ask_wv.drop(["time", "Symbol"], axis=1, inplace=True)

    ax1 = mpf.make_addplot(ask_wv["vwap"])
    fig = mpf.plot(ask_wv, type="candle", title=symbol, addplot=ax1, savefig="vwap.png")
    send_image(image_file="vwap.png")
    return [ask_wv["vwap"], ask_wv]

if __name__ == "__main__":
    get_monthly_rets()
