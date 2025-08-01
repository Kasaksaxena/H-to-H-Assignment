import pandas as pd 
import yfinance as yf
from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator,MACD

stocks=["RELIANCE.NS","TCS.NS","INFY.NS"]

def fetch_data(ticker):
    df=yf.download(ticker,period="6mo",interval="1d",auto_adjust=True)
    df=df[["Close"]]
    df.dropna(inplace=True)
    
    df["Close"]=pd.to_numeric(df["Close"].squeeze(),errors="coerce")
    df.dropna(inplace=True)
    return df

def add_indicator(df):
    df=df.copy() 
    close_series=df["Close"].squeeze()
    
    df["RSI"]=RSIIndicator(close=close_series,window=14).rsi()
    df["SMA20"]=SMAIndicator(close=close_series,window=20).sma_indicator()
    df["SMA50"]=SMAIndicator(close=close_series,window=50).sma_indicator()
    df["MACD"]=MACD(close=close_series).macd()
    df["MACD_Signal"]=MACD(close=close_series).macd_signal()
    df["MACD_Diff"]=MACD(close=close_series).macd_diff()
    
    df.dropna(inplace=True)
    return df
    
    
    
    

if __name__=="__main__":
    for stock in stocks:
        df=fetch_data(stock)
        df=add_indicator(df)
        df.dropna(inplace=True)
        df.to_csv(f"{stock}_indicators.csv",index=True)
        print(f"{stock} done. Rows:{len(df)}")
    
    