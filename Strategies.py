import backtrader as bt

class MACDAndMACross(bt.Strategy):

    def __init__(self):
        self.close = self.datas[0].close
        self.macd = bt.indicators.MACD()
        self.signal = self.macd.lines.signal
        self.ma_fast = bt.indicators.MovingAverageSimple(period=5)
        self.ma_slow = bt.indicators.MovingAverageSimple(period=6)
        self.ma_cross = bt.indicators.CrossOver(self.ma_fast, self.ma_slow)

    def next(self):
        if not self.position:
            if self.macd[0] < 0 and self.macd[0] > self.signal[0]:
                size = int(self.broker.getcash() / self.close[0])
                self.buy(size=size)
        else:
            if self.macd[0] > 0 and self.macd[0] < self.signal[0]*0.9:
                self.sell(size=self.position.size)
