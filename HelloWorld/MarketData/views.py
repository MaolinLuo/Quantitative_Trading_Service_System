from django.http import HttpResponse
import json
import akshare as ak
import pandas as pd
import datetime


def UDdistribution(request):
    stock_zh_a_spot_em_df = ak.stock_zh_a_spot_em()
    record = [0,0,0,0,0,0,0,0,0,0]
    UpDown = stock_zh_a_spot_em_df.loc[:, ["涨跌幅"]]
    for row in UpDown.iterrows():
        if float(row[1]) < -8:
            record[0] = record[0] + 1
        elif float(row[1]) < -6:
            record[1] = record[1] + 1
        elif float(row[1]) < -4:
            record[2] = record[2] + 1
        elif float(row[1]) < -2:
            record[3] = record[3] + 1
        elif float(row[1]) < 0:
            record[4] = record[4] + 1
        elif float(row[1]) < 2:
            record[5] = record[5] + 1
        elif float(row[1]) < 4:
            record[6] = record[6] + 1
        elif float(row[1]) < 6:
            record[7] = record[7] + 1
        elif float(row[1]) < 8:
            record[8] = record[8] + 1
        elif float(row[1]) >=8:
            record[9] = record[9] + 1
    jsonArr = json.dumps(record, ensure_ascii=False)
    return HttpResponse(jsonArr) # 涨跌分布拉取成功

def StockIndex(request):
    marketlist = ['深证成指', '上证指数','创业板指']
    stock_index = ak.stock_zh_index_spot()
    stock_index = stock_index.loc[stock_index['名称'].isin(marketlist)]
    stock_index = stock_index.loc[:, ['最新价','涨跌额','涨跌幅']]
    stock_index.columns = ['latest_price', 'change_amount', 'change']
    js = stock_index.to_json(orient = 'index')
    return HttpResponse(js) # 股票指数拉取成功

def MostPopular(request):
    stock_hot_follow_xq_df = ak.stock_hot_follow_xq(symbol="最热门")
    df = stock_hot_follow_xq_df.head(10)
    return HttpResponse(df.to_json()) # 关注度拉取成功

def HistoryStockIndex(request):
    ISOTIMEFORMAT = '%Y%m%d'
    date_now = datetime.datetime.now().strftime(ISOTIMEFORMAT)
    index_zh_a_hist_df_sh = ak.index_zh_a_hist(symbol="000001", period="daily", start_date="20220101", end_date=date_now)
    index_zh_a_hist_df_sz = ak.index_zh_a_hist(symbol="399001", period="daily", start_date="20220101", end_date=date_now)
    index_zh_a_hist_df_cy = ak.index_zh_a_hist(symbol="399006", period="daily", start_date="20220101", end_date=date_now)
    index_zh_a_hist_df_sh = index_zh_a_hist_df_sh.drop(['开盘', '最高', '最低', '成交量', '成交额', '振幅', '涨跌幅', '涨跌额', '换手率'], axis=1)
    index_zh_a_hist_df_sz = index_zh_a_hist_df_sz.drop(['日期', '开盘', '最高', '最低', '成交量', '成交额', '振幅', '涨跌幅', '涨跌额', '换手率'], axis=1)
    index_zh_a_hist_df_cy = index_zh_a_hist_df_cy.drop(['日期', '开盘', '最高', '最低', '成交量', '成交额', '振幅', '涨跌幅', '涨跌额', '换手率'], axis=1)
    result = pd.concat([index_zh_a_hist_df_sh,index_zh_a_hist_df_sz,index_zh_a_hist_df_cy], axis=1)
    result.columns = ['日期','上证指数', '深证指数','创业板指']
    js = result.to_json(orient = 'index', force_ascii=False)
    return HttpResponse(json.dumps(js,ensure_ascii=False)) # 历史股票指数拉取成功
