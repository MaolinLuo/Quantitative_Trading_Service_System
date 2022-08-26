from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import akshare as ak

import timeit
import datetime
import tushare as ts
import pandas as pd
import backtrader as bt
import backtrader.feeds as btfeeds
import backtrader.indicators as btind
import datetime

token="076d7a87e591cad66956800e5e7c65521ed46b2ce008422eec40dcc5"
trade_dict=dict() #暂存每轮的交易，每轮结束后push到trade_result中
trade_result=pd.DataFrame(columns=['date','code','status','size','price','transaction'])
hold_dict=dict()
hold_result=pd.DataFrame(columns=['date','code','size','price','present','profit'])
date_value_list=[]


def get_benchmark(startdate,enddate):
    index_zh_a_hist_df = ak.index_zh_a_hist(symbol="000300", period="daily", start_date=startdate, end_date=enddate)
    df = index_zh_a_hist_df[['日期','涨跌幅']]
    df.columns = ['date','QuoteChange']
    return df


def getdata(ts_code):
    pro = ts.pro_api(token)
    ISOTIMEFORMAT = '%Y%m%d'
    date_now = datetime.datetime.now().strftime(ISOTIMEFORMAT)
    df = pro.daily(ts_code=ts_code, start_date="20150101", end_date=date_now).sort_values('trade_date')
    df.index=pd.to_datetime(df["trade_date"])
    df=df[["open","high","low","close"]]
    return df
def return_hold_dict(pos,data):


    hold_dict['date'] = data.datetime.date(0).strftime('%Y-%m-%d')

    hold_dict['code'] = data._name
    hold_dict['size'] = pos.size
    hold_dict['price'] = pos.price
    hold_dict['present'] = pos.adjbase
    hold_dict['profit'] = pos.size * (pos.adjbase - pos.price)
    temp = pd.DataFrame(hold_dict, index=[0])
    return temp
def return_trade_dict(data,type,size):
    trade_dict['date'] = data.datetime.date(0).strftime('%Y-%m-%d')

    trade_dict['code'] = data._name
    trade_dict['status'] = type
    trade_dict['size'] = size
    trade_dict['price'] = data.close[0]
    trade_dict['transaction'] = size * data.close
    temp = pd.DataFrame(trade_dict, index=[0])
    return temp
def calculate_date_profit(value_ratio,list):

    value_ratio.append([list[0][0].strftime('%Y-%m-%d'),0.0])
    for i in range(1, len(list)):
        value_ratio.append([list[i][0].strftime('%Y-%m-%d'),(list[i][1] - list[0][1]) / list[0][1]])
    value_ratio=pd.DataFrame(value_ratio,columns=["date","ratio"])
    return value_ratio
def add_custom_analyzer(cerebro):
    cerebro.addanalyzer(bt.analyzers.Returns, _name="returns")
    cerebro.addanalyzer(bt.analyzers.SharpeRatio,_name="sharpe")
    cerebro.addanalyzer(bt.analyzers.DrawDown,_name="drawdown")
    cerebro.addanalyzer(bt.analyzers.AnnualReturn,_name="annualreturn")

    cerebro.addanalyzer(bt.analyzers.SharpeRatio_A,_name="annualsharpe")

def return_indicators_list(strat,indicator_list):
    indicator_list.append(strat.analyzers.returns.get_analysis()['rtot'])
    indicator_list.append(strat.analyzers.returns.get_analysis()['rnorm100'])
    indicator_list.append(strat.analyzers.drawdown.get_analysis()['max']['drawdown'])
    indicator_list.append(strat.analyzers.drawdown.get_analysis()['max']['moneydown'])
    indicator_list.append(strat.analyzers.annualsharpe.get_analysis()['sharperatio'])

    return indicator_list
def return_transaction(strat):
    result=strat.analyzers.tran.get_analysis()
    print(result.value())




