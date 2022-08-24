import json
from dateutil.relativedelta import relativedelta
from django.http import HttpResponse
import datetime
import akshare as ak
from jqdatasdk import *

auth('13383909875', '13383909875Zc')

def hello(request):
    return HttpResponse("Hello world!")

# 获取k线图上所需数据
def kline(request):
    if request.headers['Content-Type'] == "application/json;charset=UTF-8":
        data = json.loads(request.body.decode('utf-8'))
        code = data.get('code')
    else:
        code = request.GET.get("code")
    # 判断有无该股票
    ncode = normalize_code(code)  # 转成聚宽的代码
    try:
        display_name = get_security_info(ncode).display_name
    except:
        return HttpResponse(json.dumps({'code':'222'}))
    # 获取当天日期和两年前的日期
    today = datetime.date.today()
    ftoday = '20' + today.strftime('%y%m%d')
    before = (datetime.datetime.now() - relativedelta(years=2)).strftime("%Y%m%d")
    # 调用akshare的数据
    stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=code, period="daily",
                                            start_date=before, end_date=ftoday, adjust="")
    df = stock_zh_a_hist_df.loc[:, '日期':'成交量']
    df.columns = ['trade_date', 'open', 'close', 'high', 'low', 'vol']
    df['ma5'] = df.close.rolling(window=5).mean()
    df['ma10'] = df.close.rolling(window=10).mean()
    df['ma20'] = df.close.rolling(window=20).mean()
    df['ma30'] = df.close.rolling(window=30).mean()
    # print(df)
    return HttpResponse(df.to_json())

def allStocks(request):
    if request.headers['Content-Type'] == "application/json;charset=UTF-8":
        data = json.loads(request.body.decode('utf-8'))
        pagenum = data.get('pagenum')
    else:
        pagenum = request.GET.get("pagenum")
    # 调用akshare的数据
    stock_zh_a_spot_em_df = ak.stock_zh_a_spot_em()
    df = stock_zh_a_spot_em_df.loc[:, '序号':'成交量']
    df.columns = ['num', 'code', 'name', 'price', 'range', 'amount', 'vol']
    if pagenum == "102":
        df = df[(int(pagenum) - 1) * 50:5092]
    else:
        df = df[(int(pagenum) - 1) * 50:(int(pagenum) - 1) * 50 + 50]
    res = []
    i = 0
    while i != len(df):
        tmp = {"number": str(df.iat[i, 0]), "code": str(df.iat[i, 1]), "stock_name": df.iat[i, 2],
               "present_price": str(df.iat[i, 3]),
               "change_percent": str(df.iat[i, 4]), "change_volume": str(df.iat[i, 5]),
               "trade_volume": str(df.iat[i, 6])}
        res.append(tmp)
        i += 1
    return HttpResponse(json.dumps(res))
    # return HttpResponse(df.to_json())

def realTableData(request):
    if request.headers['Content-Type'] == "application/json;charset=UTF-8":
        data = json.loads(request.body.decode('utf-8'))
        code = data.get('code')
    else:
        code = request.GET.get("code")
    # 判断有无该股票
    ncode = normalize_code(code)  # 转成聚宽的代码
    try:
        display_name = get_security_info(ncode).display_name
    except:
        return HttpResponse(json.dumps({'code': '222'}))
    df = ak.stock_zh_a_spot_em()
    df = df.loc[df['代码'] == code]
    df = df.loc[:, ('最新价', '今开', '涨跌额', '最高', '涨跌幅', '名称')]
    res = []
    res.append({"最新价": df.iat[0, 0], "开盘价": df.iat[0, 1], "涨跌": df.iat[0, 2], "最高价": df.iat[0, 3],
                "涨跌幅": str(df.iat[0, 4]) + '%', "名称": df.iat[0, 5]})
    return HttpResponse(json.dumps(res))

# 轮子，工具函数，数字转xx万
def str_of_num(num):
    '''
    递归实现，精确为最大单位值 + 小数点后三位
    '''

    def strofsize(num, level):
        if level >= 2:
            return num, level
        elif num >= 10000:
            num /= 10000
            level += 1
            return strofsize(num, level)
        else:
            return num, level

    units = ['', '万', '亿']
    num, level = strofsize(num, 0)
    if level > len(units):
        level -= 1
    return '{}{}'.format(round(num, 1), units[level])

def realBaseData(request):
    if request.headers['Content-Type'] == "application/json;charset=UTF-8":
        data = json.loads(request.body.decode('utf-8'))
        code = data.get('code')
    else:
        code = request.GET.get("code")
    # 判断有无该股票
    ncode = normalize_code(code)  # 转成聚宽的代码
    try:
        display_name = get_security_info(ncode).display_name
    except:
        return HttpResponse(json.dumps({'code': '222'}))
    df = ak.stock_zh_a_spot_em()
    df = df.loc[df['代码'] == code]
    df = df.loc[:, ('换手率', '成交量', '量比', '成交额', '流通市值', '总市值', '市盈率-动态', '涨速')]
    res = []
    res.append({"换手": str(df.iat[0, 0]) + '%', "成交量": str_of_num(df.iat[0, 1]), "量比": df.iat[0, 2],
                "成交额": str_of_num(df.iat[0, 3]), "流通市值": str_of_num(df.iat[0, 4]),
                "总市值": str_of_num(df.iat[0, 5]), "市盈率": df.iat[0, 6], "涨速": df.iat[0, 7]})
    return HttpResponse(json.dumps(res))

def companyinfo(request):
    if request.headers['Content-Type'] == "application/json;charset=UTF-8":
        data = json.loads(request.body.decode('utf-8'))
        code = data.get('code')
    else:
        code = request.GET.get("code")
    # 判断有无该股票
    ncode = normalize_code(code)  # 转成聚宽的代码
    try:
        display_name = get_security_info(ncode).display_name
    except:
        return HttpResponse(json.dumps({'code': '222'}))
    q = query(finance.STK_COMPANY_INFO).filter(finance.STK_COMPANY_INFO.code == normalize_code(code)).limit(10)
    df = finance.run_query(q)
    # print(df)
    return HttpResponse(df.to_json(orient='records'))
