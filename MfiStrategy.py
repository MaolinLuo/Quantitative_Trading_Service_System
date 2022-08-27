import math

from utils.util import *
class TusharePdData(bt.feeds.PandasData):


    params = (
        ('datetime', None),
        ('open', -1),
        ('high', -1),
        ('low', -1),
        ('close', -1),
        ('volume', 9),
        ('openinterest', -1),
    )
class MFI(bt.Indicator):
    lines=("mfi","raw_mf","typical","money_flow_pos","money_flow_neg")
    def next(self):
        #计算mfi
        typical_price=(self.data.close[0]+self.data.low[0]+self.data.high[0])/3
        self.lines.typical[0]=typical_price
        raw_mf=self.lines.typical[0]*self.data.volume[0]
        self.lines.raw_mf[0]=raw_mf
        self.lines.money_flow_pos[0]=raw_mf if self.lines.typical[0]>=self.lines.typical[-1] else 0
        self.lines.money_flow_neg[0] = raw_mf if self.lines.typical[0] <= self.lines.typical[-1] else 0
        pos_mf=math.fsum(self.lines.money_flow_pos.get(size=14))
        neg_mf =math.fsum(self.lines.money_flow_neg.get(size=14))

        if neg_mf==0:
            self.lines.mfi[0]=100
            return
        self.lines.mfi[0]=100-100/(1+pos_mf/neg_mf)



class MfiStrategy(bt.Strategy):
    def __init__(self):
         # self.typical=dict()
         # self.raw_mf=dict()
         # self.money_flow_pos=dict()
         # self.money_flow_neg=dict()
         # self.mfi=dict()
         self.Mfi=dict()
         for data in self.datas:
           self.Mfi[data._name]=MFI(data)


    def next(self):
           global trade_result
           global hold_result
           global date_value_list
           for data in self.datas:
            pos=self.getposition(data)
            if pos.size==0:
            # 低于35，买入
                if self.Mfi[data._name][0]<35:
                    stakesize=int(self.broker.getcash()/data.close*0.4)
                    self.order=self.buy(data,size=stakesize)
                    print(data._name)
                    temp = return_trade_dict(data, "buy", stakesize)
                    trade_result = pd.concat([temp, trade_result])
            elif pos.size>0:
                #大于65，卖出
                if self.Mfi[data._name][0]>65:
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
            date_value_list.append((self.data.datetime.date(0), self.broker.getvalue()))
    def log(self, txt, dt=None):

        dt = dt or self.data.datetime.date(0)

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


def run_mfi(ts_code_list,startdate,enddate):
    cerebro=bt.Cerebro()
    cerebro.addstrategy(MfiStrategy)
    start_year = int(startdate[0:4])
    start_month = int(startdate[4:6])
    start_day = int(startdate[6:8])
    end_year = int(enddate[0:4])
    end_month = int(enddate[4:6])
    end_day = int(enddate[6:8])
    for ts_code in ts_code_list:
     stock=getmsidata(ts_code)
     data = TusharePdData(dataname=stock, fromdate=datetime.date(start_year, start_month, start_day), todate=datetime.date(end_year, end_month, end_day))
     cerebro.adddata(data,name=ts_code)
    cerebro.broker.setcash(1000000)
    cerebro.broker.setcommission(commission=0.001)
    add_custom_analyzer(cerebro)
    result=cerebro.run()

    strat=result[0]
    indicator_list=[cerebro.broker.getvalue()]
    indicator_list=return_indicators_list(strat,indicator_list)


    value_ratio=return_value_ratio(strat)#计算每天的策略收益
    print(cerebro.broker.getvalue())
    print(value_ratio)
    return hold_result.sort_values('date'),trade_result.sort_values('date'),value_ratio,indicator_list
run_mfi(["600519.SH","000001.SZ"],"20190101","20220320")