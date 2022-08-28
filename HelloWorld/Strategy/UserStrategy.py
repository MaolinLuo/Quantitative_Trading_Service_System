
from . import util
import backtrader as bt
import pandas as pd

class UserStrategy(bt.Strategy):

    params = (
        ('period_sma10', 10),
        ('period_sma30', 30),
        ('stakesize',0)
    )

    # ��ӡ��־
    def log(self, txt, dt=None):

        dt = dt or self.data.datetime.date(0)

        print('%s, %s' % (dt, txt))

    def __init__(self):

        # ���ڱ��涩��
        self.order = None
        # �����۸�
        self.buyprice = None
        # ����Ӷ��
        self.buycomm = None

        self.sma10=dict()
        self.sma30=dict()
        for data in self.datas:
        # ����10�վ�

         self.sma10[data._name] = util.btind.MovingAverageSimple(data.close, period=self.params.period_sma10)
        # ����30�վ�
         self.sma30[data._name] = util.btind.MovingAverageSimple(data.close, period=self.params.period_sma30)

    def notify_order(self, order):


        # �ȴ������ύ������cerebro����
        if order.status in [order.Submitted, order.Accepted]:
            return

        # �ȴ��������
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

        # ���������֤���㣬��������ɣ�����ִ���¾ܾ���
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):

        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))  # pnl��ӯ  pnlcomm����

    # �����߼�ʵ��
    def next(self):
        global date_value_list  #essential
        global trade_result # essential
        global hold_result #essential
        for data in self.datas:
            pos = self.getposition(data)
            # �������10�վ��ߴ�30�վ��߲��������10�վ���С30�վ��ߣ����Ҹù�Ʊû�г�,������г�����
            if pos.size==0:
                if self.sma10[data._name][0] > self.sma30[data._name][0] and self.sma10[data._name][-1] < self.sma30[data._name][-1]:
                    # �ж϶�������ɣ������ΪNone������Ϊ������Ϣ
                    if self.order:
                        return


                    # ���϶���������ɣ��ɼ���ִ�����
                    self.params.stakesize = int(self.broker.getcash()/data.close*0.4)
                    self.order = self.buy(data=data,size=self.params.stakesize)
                    #����ÿ�ֽ����б�,essential
                    temp=util.return_trade_dict(data,"buy",self.params.stakesize)

                    util.trade_result = pd.concat([temp, util.trade_result])

            # �������10�վ���С30�վ��߲��������10�վ��ߴ�30�վ��ߣ�����г�������

            elif pos.size>0: #essential,����Ҫ�д˹�Ʊ�Ƿ�ֲ֣�����ֲֲ���

                if self.sma10[data._name][0] < self.sma30[data._name][0] and self.sma10[data._name][-1] > self.sma30[data._name][-1]:
                    # ����
                    self.params.stakesize = 5000
                    if(pos.size-self.params.stakesize>=0): #���������������Ǵ��ڳֲ�����
                        self.order = self.sell(data=data,size=self.params.stakesize)
                        #����ÿ�ֵĽ�����,essential
                        temp=util.return_trade_dict(data,"sell",self.params.stakesize)
                        util.trade_result = pd.concat([temp, util.trade_result])
                    else:  #��������ڣ���ֱ����֣�����ʹ�����漴��������������
                        self.params.stakesize=pos.size
                        self.order = self.sell(data=data, size=self.params.stakesize)
                        #����ÿ�ֽ����б�,essential
                        temp=util.return_trade_dict(data,"sell",self.params.stakesize)
                        util.trade_result = pd.concat([temp, util.trade_result])

        # ÿ�����������󣬿��ֲֵĹ�Ʊ,essential
        for data in self.datas:

            pos = self.getposition(data)

            if len(pos):
                # ��ֲ���
                temp=util.return_hold_dict(pos,data)
                util.hold_result = pd.concat([temp, util.hold_result])
     

def run_user(ts_code_list=['000001.SZ','000002.SZ'],startdate='20220419',enddate='20220821'):
    cerebro=bt.Cerebro()
    cerebro.addstrategy(UserStrategy)
    start_year = int(startdate[0:4])
    start_month = int(startdate[4:6])
    start_day = int(startdate[6:8])
    end_year = int(enddate[0:4])
    end_month = int(enddate[4:6])
    end_day = int(enddate[6:8])
    for ts_code in ts_code_list:
        stock=util.getdata(ts_code)
        data = util.btfeeds.PandasData(dataname=stock, fromdate=util.datetime.date(start_year, start_month, start_day), todate=util.datetime.date(end_year, end_month, end_day))
        cerebro.adddata(data,name=ts_code)
    benchmark=util.get_benchmark(startdate,enddate)
    cerebro.broker.setcash(1000000)
    cerebro.broker.setcommission(commission=0.001)
    util.add_custom_analyzer(cerebro)
    old_value=cerebro.broker.getvalue()
    result = cerebro.run()
    strat = result[0]
    indicator_list = [cerebro.broker.getvalue(),(cerebro.broker.getvalue()-old_value)/old_value]
    indicator_list = util.return_indicators_list(strat, indicator_list)

    
    value_ratio=util.return_value_ratio(strat)#����ÿ��Ĳ�������
    return util.hold_result.sort_values('date'),util.trade_result.sort_values('date'),value_ratio,benchmark,indicator_list


    # hold_result:ÿ�ճֲ�&����
    # trade_result:��������
    # value_ratio:ÿ�ղ�������,����������ͼ
    # indicator_list:��Ԫ�ر�ʾʣ��ֲּ�ֵ������Ԫ�ر�ʾ����������,����Ԫ�ر�ʾ�ٷ�����ʾ�껯�����ʣ��ĺ�Ԫ�ر�ʾ���س��ʣ����Ԫ�ر�ʾ���س���
    #��Ԫ���껯�ձ���

