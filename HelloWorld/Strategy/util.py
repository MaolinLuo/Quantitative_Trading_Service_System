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
    hold_dict['size'] = pos.size#持仓数量
    hold_dict['price'] = pos.price #成本价
    hold_dict['present'] = pos.adjbase#现价
    hold_dict['profit'] = pos.size * (pos.adjbase - pos.price)#盈亏
    temp = pd.DataFrame(hold_dict, index=[0])
    return temp
def return_trade_dict(data,type,size):
    trade_dict['date'] = data.datetime.date(0).strftime('%Y-%m-%d')

    trade_dict['code'] = data._name
    trade_dict['status'] = type#买卖
    trade_dict['size'] = size#成交量
    trade_dict['price'] = data.close[0]#成交单价
    trade_dict['transaction'] = size * data.close#成交总额
    temp = pd.DataFrame(trade_dict, index=[0])
    return temp

def add_custom_analyzer(cerebro):
    cerebro.addanalyzer(bt.analyzers.Returns, _name="returns")
    cerebro.addanalyzer(bt.analyzers.SharpeRatio,_name="sharpe")
    cerebro.addanalyzer(bt.analyzers.DrawDown,_name="drawdown")
    cerebro.addanalyzer(bt.analyzers.AnnualReturn,_name="annualreturn")

    cerebro.addanalyzer(bt.analyzers.SharpeRatio_A,_name="annualsharpe")
    cerebro.addanalyzer(bt.analyzers.TimeReturn,_name="timereturn")

def return_indicators_list(strat,indicator_list):
    indicator_list.append(strat.analyzers.returns.get_analysis()['rtot'])
    indicator_list.append(strat.analyzers.returns.get_analysis()['rnorm100'])
    indicator_list.append(strat.analyzers.drawdown.get_analysis()['max']['drawdown'])
    indicator_list.append(strat.analyzers.drawdown.get_analysis()['max']['moneydown'])
    indicator_list.append(strat.analyzers.annualsharpe.get_analysis()['sharperatio'])

    return indicator_list
def return_transaction(strat):
    result=strat.analyzers.tran.get_analysis()

def return_value_ratio(strat):
    d=strat.analyzers.timereturn.get_analysis()
    df = pd.DataFrame(list(d.items()), columns=['date', 'ratio'])
    df['date'] = df['date'].apply(lambda x : x.strftime('%Y-%m-%d'))
    
    return df


