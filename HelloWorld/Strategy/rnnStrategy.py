from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import datetime
from pyexpat import model
import tushare as ts
import pandas as pd
import backtrader as bt
import backtrader.feeds as btfeeds
import backtrader.indicators as btind
from . import evaluationRNN
import torch
from . import util


token="96dfb6f8b1fd4d5e4972d66a49f72523746fd493cc56d921675a406a"
def get_data(ts_code,startdate,enddate):
    pro = ts.pro_api(token)

    df = pro.daily(ts_code=ts_code, start_date=startdate, end_date=enddate).sort_values('trade_date')
    df.index=pd.to_datetime(df["trade_date"])
    df=df[["trade_date","ts_code","open","close"]]
    return df

steps = 1
rate = 0.03
stock_size = 100

class DLStrategy(bt.Strategy):

    # 打印日志
    def log(self, txt, dt=None):
        # 记录策略的执行日志
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):

        self.model = torch.load('./rnn.pt')
        print('model loaded')

        # 用于保存订单
        self.order = None
        # 订单价格
        self.buyprice = None
        # 订单佣金
        self.buycomm = None

        # 定义变量保存所有收盘价
        self.dataclose = self.data.close

    # 订单状态通知，买入卖出都是下单
    def notify_order(self, order):

        # 等待订单提交、订单被cerebro接受
        if order.status in [order.Submitted, order.Accepted]:
            # broker 提交/接受了，买/卖订单则什么都不做
            return

        # 检查一个订单是否完成
        # 注意: 当资金不足时，broker会拒绝订单
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    '已买入, 价格: %.2f, 费用: %.2f, 佣金 %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            elif order.issell():
                self.log('已卖出, 价格: %.2f, 费用: %.2f, 佣金 %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))
            # 记录当前交易数量
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('订单取消/保证金不足/拒绝')

        # 其他状态记录为：无挂起订单
        self.order = None


    # 交易状态通知，一买一卖算交易
    def notify_trade(self, trade):

        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))  # pnl：盈利  pnlcomm：手续费


    # 策略逻辑实现
    def next(self):
        # 记录收盘价
        global hold_result
        global trade_result
        global date_value_list
        self.log('Close, %.2f' % self.dataclose[0])
        # 如果有订单正在挂起，不操作
        if self.order:
            return

        global steps
        global rate
        global stock_size
        self.model.to('cpu')
        self.model.eval()
        stock_list = []
        for i in list(range(-steps+1, 1, 1)):
            stock_list.append(self.dataclose[i])
        stock_list = torch.tensor(stock_list)
        stock_list = stock_list.unsqueeze(0).unsqueeze(-1)
        y_hat, _ = self.model(stock_list)
        y_hat = y_hat.tolist()[0]

        # 如果没有持仓则买入
        pos = self.getposition()

        if pos.size==0:

            print(y_hat)
            print(self.dataclose[0])
            if (y_hat - self.dataclose[0])/self.dataclose[0] > rate:
                # 买入
                self.log('买入单, %.2f' % self.dataclose[0])
                # 跟踪订单避免重复
                self.order = self.buy(size=stock_size)
                temp = util.return_trade_dict(self.datas[0], "buy", stock_size)
                util.trade_result = pd.concat([temp, util.trade_result])

        elif pos.size>0:
            # 如果已经持仓，且当前交易数据量在买入后steps个单位后
            if len(self) >= (self.bar_executed + steps):
                # 全部卖出
                self.log('卖出单, %.2f' % self.dataclose[0])
                # 跟踪订单避免重复
                self.order = self.sell(size=pos.size)
                temp = util.return_trade_dict(self.datas[0], "sell", stock_size)
                util.trade_result = pd.concat([temp, util.trade_result])

        if len(pos):
         temp = util.return_hold_dict(pos, self.datas[0])
         util.hold_result = pd.concat([temp, util.hold_result])

        util.date_value_list.append((self.data.datetime.date(0), self.broker.getvalue()))


def run_rnn(ts_code,startdate,enddate):
     # 创建Cerebro引擎
     cerebro = bt.Cerebro()
     # Cerebro引擎在后台创建broker(经纪人)，系统默认资金量为10000

     # 为Cerebro引擎添加策略
     cerebro.addstrategy(DLStrategy)

     # 创建交易数据集
     stock = get_data(ts_code, startdate, enddate)
     start_year = int(startdate[0:4])
     start_month = int(startdate[4:6])
     start_day = int(startdate[6:8])
     end_year = int(enddate[0:4])
     end_month = int(enddate[4:6])
     end_day = int(enddate[6:8])
     data = bt.feeds.PandasData(
         dataname=stock,
         # 数据必须大于fromdate
         fromdate=datetime.datetime(start_year, start_month, start_day),
         # 数据必须小于todate
         todate=datetime.datetime(end_year, end_month, end_day))

     # 加载交易数据
     cerebro.adddata(data)
     benchmark=util.get_benchmark(startdate,enddate)
     # 设置投资金额100000.0
     cerebro.broker.setcash(1000000.0)
     # # 设置佣金为0.001,除以100去掉%号
     cerebro.broker.setcommission(commission=0.001)

     util.add_custom_analyzer(cerebro)
     old_value=cerebro.broker.getvalue()
     result = cerebro.run()
     strat = result[0]
     indicator_list = [cerebro.broker.getvalue(),(cerebro.broker.getvalue()-old_value)/old_value]
     indicator_list = util.return_indicators_list(strat, indicator_list)

     value_ratio = []
     value_ratio = util.calculate_date_profit(value_ratio, util.date_value_list)  # 计算每天的策略收益

     return util.hold_result.sort_values('date'), util.trade_result.sort_values('date'), value_ratio, benchmark, indicator_list

def run_rnn_final(ts_code,test_start_date,test_end_date,epoch,_steps,_rate,_stock_size):
    global steps
    steps = _steps
    global rate
    rate = _rate
    global stock_size
    stock_size = _stock_size
    evaluationRNN.prepareModel(ts_code=ts_code, start_date='20150101', end_date=test_start_date, train_test_rate=0.95, epoch=epoch,
                 steps=steps)
    result = run_rnn(ts_code, test_start_date, test_end_date)
    return result


# if __name__ == '__main__':
#     run_rnn_final('002169.SZ', '20200101', '20220824',100,3)