import yfinance as yf
import pandas as pd
from tqdm import tqdm

spy_list = pd.read_csv("spy.csv")
for ticker in tqdm(spy_list['Ticker'][0:100]):
    data = yf.download(ticker, start="2017-01-01", end="2021-10-14")
    data.to_csv("spy/%s.csv" % ticker)