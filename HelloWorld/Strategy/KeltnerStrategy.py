
from . import util
import backtrader as bt
import pandas as pd

class KeltnerStrategy(bt.Strategy):
    params=dict(
    ema=20,atr=17
    )
    def __init__(self):
        self.expo=dict()
        self.TR=dict()
        self.ATR=dict()
        self.upper=dict()
        self.lower=dict()
        for data in self.datas:
            self.expo[data._name]=util.btind.EMA(data.close,period=self.params.ema)
            self.TR[data._name] = bt.indicators.Max((data.high(0) - data.low(0)), abs(data.close(-1) - data.high(0)),
                                                    abs(data.close(-1) - data.low(0)))
            self.ATR[data._name] = bt.indicators.SimpleMovingAverage(self.TR[data._name], period=self.params.atr)
            self.upper[data._name]=self.expo[data._name]+self.ATR[data._name]
            self.lower[data._name]=self.expo[data._name]-self.ATR[data._name]
            print(self.lower[data._name](0))
    def next(self):
        global trade_result
        global hold_result
        global date_value_list
        for data in self.datas:
            pos=self.getposition(data)
            if pos.size==0:
                if data.close>self.upper[data._name]:

                    stakesize=int(self.broker.getcash()/data.close*0.8)
                    self.order = self.buy(data,size=stakesize)
                    temp = util.return_trade_dict(data, "buy", pos.size)
                    util.trade_result = pd.concat([temp, util.trade_result])
            elif pos.size>0:
                if data.close<self.expo[data._name]:
                    self.order=self.sell(data,size=pos.size)
                    temp = util.return_trade_dict(data, "sell", pos.size)
                    util.trade_result = pd.concat([temp, util.trade_result])
        for data in self.datas:

            pos = self.getposition(data)

            if len(pos):
                # 存持仓列表
                temp = util.return_hold_dict(pos, data)
                util.hold_result = pd.concat([temp, util.hold_result])

        
    def notify_order(self, order):


        # 等待订单提交、订单被cerebro接受
        if order.status in [order.Submitted, order.Accepted]:
            return

        # 等待订单完成
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))



            else:
                self.log(
                    'SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

        # 如果订单保证金不足，将不会完成，而是执行以下拒绝程序
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):

        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))  # pnl：盈利  pnlcomm：手续费
    def log(self, txt, dt=None):
        dt = dt or self.data.datetime.date(0)
        util.trade_dict['date'] = dt
        print('%s, %s' % (dt, txt))


def run_keltner(ts_code_list,startdate,enddate):
    cerebro = bt.Cerebro()
    cerebro.addstrategy(KeltnerStrategy)
    start_year = int(startdate[0:4])
    start_month = int(startdate[4:6])
    start_day = int(startdate[6:8])
    end_year = int(enddate[0:4])
    end_month = int(enddate[4:6])
    end_day = int(enddate[6:8])
    for ts_code in ts_code_list:
        stock = util.getdata(ts_code)
        data = util.btfeeds.PandasData(dataname=stock, fromdate=util.datetime.date(start_year, start_month, start_day),
                                  todate=util.datetime.date(end_year, end_month, end_day))
        cerebro.adddata(data, name=ts_code)
    benchmark=util.get_benchmark(startdate,enddate)
    cerebro.broker.setcash(1000000)
    cerebro.broker.setcommission(commission=0.001)
    util.add_custom_analyzer(cerebro)
    old_value=cerebro.broker.getvalue()
    result = cerebro.run()
    strat = result[0]
    indicator_list = [cerebro.broker.getvalue(),(cerebro.broker.getvalue()-old_value)/old_value]
    indicator_list = util.return_indicators_list(strat, indicator_list)

    value_ratio=util.return_value_ratio(strat)  # 计算每天的策略收益
    hold_result_temp = util.hold_result
    trade_result_temp = util.trade_result
    util.trade_result = pd.DataFrame(columns=['date', 'code', 'status', 'size', 'price', 'transaction'])
    util.hold_result = pd.DataFrame(columns=['date', 'code', 'size', 'price', 'present', 'profit'])
    return hold_result_temp.sort_values('date'), trade_result_temp.sort_values('date'), value_ratio, benchmark, indicator_list
    # hold_result,trade_result,value_ratio,indicator_list=run_keltner(["600519.SH"],"20200101","20220823")
