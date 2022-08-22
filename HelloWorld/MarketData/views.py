from django.http import HttpResponse
import json
import akshare as ak


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



