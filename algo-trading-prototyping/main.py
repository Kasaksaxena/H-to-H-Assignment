import pandas as pd
from strategy import backtest_strategy


stocks=["RELIANCE.NS","TCS.NS","INFY.NS"]


for stock in stocks:
    file_path = f"{stock}_indicators.csv"
    df = pd.read_csv(file_path, parse_dates=["Date"])
    print(df.head())
    df.columns=df.columns.str.strip()
    print(df.columns.tolist())
    print(f"{stock} columns",df.columns)
    df["Date"]=pd.to_datetime(df["Date"])
    df.set_index("Date",inplace=True)
    trades = backtest_strategy(df, stock)
    trades.to_csv(f"data/{stock}_trades.csv", index=False)