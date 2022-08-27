
from utils.util import *
class KeltnerStrategy(bt.Strategy):
    params=dict(
    ema=10,atr=17
    )
    def __init__(self):
        self.expo=dict()
        self.TR=dict()
        self.ATR=dict()
        self.upper=dict()
        self.lower=dict()
        # 初始化技术指标
        #TR=max{high_t-low_t,abs(close_t-1-high_t),abs(close_t-1,low_t)}
        # ATR是一个衡量波动性(Volatility)的指标，是TR的移动平均值,在TR基础上计算移动平均
        # EMA的计算比较简单: 当前时刻的移动平均价格，等于上一时刻的移动平均价格乘以一个动量参数，加上此时此刻的价格乘以一个系数。其中N一般设置为20个周期(period)。
        for data in self.datas:
            self.expo[data._name]=btind.EMA(data.close,period=self.params.ema)
            self.TR[data._name] = bt.indicators.Max((data.high(0) - data.low(0)), abs(data.close(-1) - data.high(0)),
                                                    abs(data.close(-1) - data.low(0)))
            self.ATR[data._name] = bt.indicators.SimpleMovingAverage(self.TR[data._name], period=self.params.atr)
            self.upper[data._name]=self.expo[data._name]+self.ATR[data._name]
            self.lower[data._name]=self.expo[data._name]-self.ATR[data._name]

    def next(self):
        global trade_result
        global hold_result
        global date_value_list
        for data in self.datas:
            pos=self.getposition(data)
            if pos.size==0:
                if data.close>self.upper[data._name]:

                    stakesize=int(self.broker.getcash()/data.close*0.4)
                    self.order = self.buy(data,size=stakesize)
                    temp = return_trade_dict(data, "buy", pos.size)
                    trade_result = pd.concat([temp, trade_result])
            elif pos.size>0:
                if data.close<self.expo[data._name]:
                    self.order=self.sell(data,size=pos.size)
                    temp = return_trade_dict(data, "sell", pos.size)
                    trade_result = pd.concat([temp, trade_result])
        for data in self.datas:

            pos = self.getposition(data)

            if len(pos):
                # 存持仓列表
                temp = return_hold_dict(pos, data)
                hold_result = pd.concat([temp, hold_result])
        # 保存每天的账户价值,essential


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
        trade_dict['date'] = dt
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
        stock = getdata(ts_code)
        data = btfeeds.PandasData(dataname=stock, fromdate=datetime.date(start_year, start_month, start_day),
                                  todate=datetime.date(end_year, end_month, end_day))
        cerebro.adddata(data, name=ts_code)
    cerebro.broker.setcash(1000000)
    cerebro.broker.setcommission(commission=0.001)
    add_custom_analyzer(cerebro)
    result = cerebro.run()
    strat = result[0]
    indicator_list = [cerebro.broker.getvalue()]
    indicator_list = return_indicators_list(strat, indicator_list)

    value_ratio = return_value_ratio(strat)  # 计算每天的策略收益
    print(value_ratio)
    print(hold_result)
    return hold_result.sort_values('date'), trade_result.sort_values('date'), value_ratio, indicator_list
hold_result,trade_result,value_ratio,indicator_list=run_keltner(["000001.SZ","000004.SZ","000002.SZ"],"20180301","20200823")
