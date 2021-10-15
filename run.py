import backtrader as bt
from Strategies import MACDAndMACross
from datetime import datetime
import pandas as pd
import os

spy_list = pd.read_csv("spy.csv")
result = {}
num_won = 0
num_lost = 0
for ticker in spy_list['Ticker'][0:100]:
    stock_csv_file = "spy/%s.csv" % ticker

    stockFeed = bt.feeds.YahooFinanceCSVData(dataname=stock_csv_file, fromdate=datetime(2020, 10, 14))

    cerebro = bt.Cerebro()
    cerebro.broker.setcash(1000000)

    cerebro.adddata(stockFeed)

    cerebro.addstrategy(MACDAndMACross)

    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="mytrade")
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='mysharpe')

    ###########
    # Start simulation
    ###########
    cerebro.broker.set_cash(100000)
    start_cash = cerebro.broker.getvalue()
    # print('Starting Portfolio Value: %.2f' % start_cash)

    try:
        cerebro.run()
    except:
        continue

    fianl_cash = cerebro.broker.getvalue()
    # print('Final Portfolio Value: %.2f' % fianl_cash)
    # print('Final Portfolio Change: %.2f' % (fianl_cash/start_cash*100-100)+"%")

    result[ticker] = (fianl_cash / start_cash * 100 - 100)
    if result[ticker] > 0:
        num_won += 1
    else:
        num_lost += 1

print('Total won: %d' % num_won)
print('Total lost: %d' % num_lost)
print('Average change: %.2f' % (sum(result.values()) / len(result.values())))

result_sorted = {k: v for k, v in sorted(result.items(), key=lambda item: item[1], reverse=True)}
print('Top 10:')
count = 0
for k, v in result_sorted.items():
    print('  %s: %.2f' % (k, v))
    count += 1
    if count >= 10:
        break
