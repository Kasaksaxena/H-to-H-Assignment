import pandas as pd

def backtest_strategy(df, stock_name):
    df = df.copy()
    position = None
    buy_price = 0
    trade_log = []

    for i in range(1, len(df)):
        # Conditions
        rsi = df['RSI'].iloc[i]
        sma20 = df['SMA20'].iloc[i]
        sma50 = df['SMA50'].iloc[i]
        prev_sma20 = df['SMA20'].iloc[i - 1]
        prev_sma50 = df['SMA50'].iloc[i - 1]

        #print(f"i={i}, RSI={rsi:.2f}, SMA20={sma20:.2f}, SMA50={sma50:.2f}, Prev_SMA20={prev_sma20:.2f}, Prev_SMA50={prev_sma50:.2f}")

        # Looser Buy condition: RSI < 45 and SMA crossover today
        if position is None:
            if (rsi < 45) and (sma20 > sma50):
                position = 'long'
                buy_price = df['Close'].iloc[i]
                buy_date = df.index[i]
                trade_log.append({
                    'Type': 'BUY',
                    'Date': buy_date,
                    'Price': buy_price
                })

        # Sell condition: RSI > 65 or SMA crossover down
        elif position == 'long':
            if (rsi > 65) or (sma20 < sma50):
                sell_price = df['Close'].iloc[i]
                sell_date = df.index[i]
                profit = sell_price - buy_price
                trade_log.append({
                    'Type': 'SELL',
                    'Date': sell_date,
                    'Price': sell_price,
                    'Profit': profit
                })
                position = None

    # Metrics
    trades = [t for t in trade_log if t['Type'] == 'SELL']
    total_profit = sum(t['Profit'] for t in trades)
    win_trades = len([t for t in trades if t['Profit'] > 0])
    total_trades = len(trades)
    win_ratio = (win_trades / total_trades) * 100 if total_trades else 0

    print(f"\nSummary for {stock_name}")
    print(f"Total Trades: {total_trades}")
    print(f"Winning Trades: {win_trades}")
    print(f"Win Ratio: {win_ratio:.2f}%")
    print(f"Total P&L: ₹{total_profit:.2f}")

    return pd.DataFrame(trade_log)