from utils.util import *
class TradeSizer(bt.Sizer):
    params = (('stake', 1),)
    def _getsizing(self, comminfo, cash, data, isbuy):
        if isbuy:
            return self.p.stake
        position = self.broker.getposition(data)
        if not position.size:
            return 0
        else:
            return position.size
        return self.p.stake
class TurtleStrategy(bt.Strategy):


    def __init__(self):
     self.order = None
     self.buyprice = 0
     self.buycomm = 0
     self.buy_size = 0
     self.buy_count = 0
     self.H_line=dict()
     self.L_line=dict()
     self.TR=dict()
     self.ATR=dict()
     self.buy_signal=dict()
     self.sell_signal=dict()
     for data in self.datas:
        self.H_line[data._name] = bt.indicators.Highest(data.high(-1), period=20)
        self.L_line[data._name] = bt.indicators.Lowest(data.low(-1), period=10)
        self.TR[data._name] = bt.indicators.Max((data.high(0) - data.low(0)), abs(data.close(-1) - data.high(0)), abs(data.close(-1) - data.low(0)))
        self.ATR[data._name]= bt.indicators.SimpleMovingAverage(self.TR[data._name], period=14)
        # 价格与上下轨线的交叉
        self.buy_signal[data._name]= bt.ind.CrossOver(data.close(0), self.H_line[data._name])
        self.sell_signal[data._name] = bt.ind.CrossOver(data.close(0), self.L_line[data._name])
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

    def next(self):

        global trade_result
        global hold_result
        global date_value_list
        if self.order:
            return
            # 入场：价格突破上轨线且空仓时
        for data in self.datas:
         if self.buy_signal[data._name] > 0 and self.buy_count == 0:

            print("buy1")
            self.buy_size = self.broker.getvalue() * 0.01 / self.ATR[data._name]
            self.buy_size = int(self.buy_size / 100) * 100
            self.sizer.p.stake = self.buy_size
            self.buy_count = 1
            self.order = self.buy()
            temp = return_trade_dict(data, "buy", self.sizer.p.stake)

            trade_result = pd.concat([temp, trade_result])
            # 加仓：价格上涨了买入价的0.5的ATR且加仓次数少于3次（含）
         elif data.close > self.buyprice + 0.5 * self.ATR[data._name][0] and self.buy_count > 0 and self.buy_count <=4:
            print("buy2")
            self.buy_size = self.broker.getvalue() * 0.01 / self.ATR[data._name]
            self.buy_size = int(self.buy_size / 100) * 100
            self.sizer.p.stake = self.buy_size
            self.order = self.buy()
            self.buy_count += 1
            temp = return_trade_dict(data, "buy", self.sizer.p.stake)

            trade_result = pd.concat([temp, trade_result])
            # 离场：价格跌破下轨线且持仓时
         elif self.sell_signal[data._name] < 0 and self.buy_count > 0:
            print("sell1")
            self.order = self.sell()
            self.buy_count = 0
            temp = return_trade_dict(data, "sell", self.sizer.p.stake)

            trade_result = pd.concat([temp, trade_result])
            # 止损：价格跌破买入价的2个ATR且持仓时
         elif data.close < (self.buyprice - 2 * self.ATR[data._name][0]) and self.buy_count > 0:
            print("sell2")
            self.order = self.sell()
            self.buy_count = 0
            temp = return_trade_dict(data, "sell", self.sizer.p.stake)

            trade_result = pd.concat([temp, trade_result])

        for data in self.datas:
            pos = self.getposition(data)

            if len(pos):
                # 存持仓列表
                temp = return_hold_dict(pos, data)
                hold_result = pd.concat([temp, hold_result])
            # 保存每天的账户价值,essential
        date_value_list.append((self.data.datetime.date(0), self.broker.getvalue()))

    def log(self, txt, dt=None):
        dt = dt or self.data.datetime.date(0)
        trade_dict['date'] = dt
        print('%s, %s' % (dt, txt))
def run_turtle(ts_code_list):
    cerebro = bt.Cerebro()
    cerebro.addstrategy(TurtleStrategy)
    #加载数据
    for ts_code in ts_code_list:
     stock = getdata(ts_code)
     data = btfeeds.PandasData(dataname=stock, fromdate=datetime.date(2020, 1, 1), todate=datetime.date(2022, 7, 11))
     cerebro.adddata(data,name=ts_code)
    cerebro.broker.setcash(1000000)
    cerebro.broker.setcommission(commission=0.001)
    cerebro.addanalyzer(bt.analyzers.TimeReturn, _name="time_return")
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name="sharpe")
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name="drawdown")
    cerebro.addanalyzer(bt.analyzers.LogReturnsRolling, _name="return_rolling")
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.addsizer(TradeSizer)
    result = cerebro.run()
    strat = result[0]
    print('Ending Portfolio Value: %.2f' % cerebro.broker.getvalue())
    print('sharperatio:', strat.analyzers.sharpe.get_analysis())
    print('drawdown:', strat.analyzers.drawdown.get_analysis()['max']['drawdown'])
    print("return_rolling:", strat.analyzers.return_rolling.get_analysis())
    print("time_return:", strat.analyzers.time_return.get_analysis())
    print(trade_result)
    print(hold_result)
    value_ratio = []
    value_ratio = calculate_date_profit(value_ratio, date_value_list)  # 计算每天的策略收益
    print(value_ratio)
    cerebro.plot()
run_turtle(["000004.SZ","000002.SZ"])


