from . import util
import backtrader as bt
import pandas as pd

class BollStrategy(bt.Strategy):
    params = (

        ('stakesize', 0),
    )
    def __init__(self):

     self.order = None
     # 订单价格
     self.buyprice = None
     # 订单佣金
     self.buycomm = None
     self.topline=dict()
     self.supportline=dict()
     #计算压力线与支撑线
     for data in self.datas:

       self.topline[data._name]=util.btind.BollingerBands(data,period=20).top
       self.supportline[data._name]=util.btind.BollingerBands(data,period=20).bot
    def next(self):

         global trade_result
         global hold_result
         global date_value_list


         for data in self.datas:

            pos=self.getposition(data)

            if pos.size==0:

                  if self.supportline[data._name]>data.close:
                   if self.order:
                       return
                   self.params.stakesize=int(self.broker.getcash()/data.close*0.3)
                   self.order = self.buy(data=data, size=self.params.stakesize)
                   temp = util.return_trade_dict(data, "buy", self.params.stakesize)

                   util.trade_result = pd.concat([temp, util.trade_result])






            elif pos.size>0:

                if self.topline[data._name]<=data.close:
                  self.params.stakesize=pos.size
                  self.order=self.sell(data=data,size=pos.size)
                  temp = util.return_trade_dict(data, "sell", self.params.stakesize)
                  util.trade_result = pd.concat([temp, util.trade_result])
         for data in self.datas:
             pos = self.getposition(data)

             if len(pos):
                 # 存持仓列表
                 temp = util.return_hold_dict(pos, data)
                 util.hold_result = pd.concat([temp, util.hold_result])


    def log(self, txt, dt=None):
        dt = dt or self.data.datetime.date(0)
        util.trade_dict['date'] = dt
        print('%s, %s' % (dt, txt))
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

                 
def run_Boll(ts_code_list,startdate,enddate):
    cerebro = bt.Cerebro()
    cerebro.addstrategy(BollStrategy)
    start_year = int(startdate[0:4])
    start_month = int(startdate[4:6])
    start_day = int(startdate[6:8])
    end_year = int(enddate[0:4])
    end_month = int(enddate[4:6])
    end_day = int(enddate[6:8])
    for ts_code in ts_code_list:
        stock = util.getdata(ts_code)
        data = util.btfeeds.PandasData(dataname=stock, fromdate=util.datetime.date(start_year, start_month, start_day), todate=util.datetime.date(end_year, end_month, end_day))
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
    
    value_ratio=util.return_value_ratio(strat)#计算每天的策略收益
    hold_result_temp = util.hold_result
    trade_result_temp = util.trade_result
    util.trade_result = pd.DataFrame(columns=['date', 'code', 'status', 'size', 'price', 'transaction'])
    util.hold_result = pd.DataFrame(columns=['date', 'code', 'size', 'price', 'present', 'profit'])
    return hold_result_temp.sort_values('date'), trade_result_temp.sort_values('date'), value_ratio, benchmark, indicator_list
