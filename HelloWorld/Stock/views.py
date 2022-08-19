import json
from dateutil.relativedelta import relativedelta
from django.http import HttpResponse
import akshare as ak
import datetime


def hello(request):
    return HttpResponse("Hello world!")

# 获取k线图上所需数据
def kline(request):
    if request.headers['Content-Type']=="application/json;charset=UTF-8":
        data=json.loads(request.body.decode('utf-8'))
        code=data.get('code')
    else:
        code = request.GET.get("code")
    # 获取当天日期和两年前的日期
    today=datetime.date.today()
    ftoday='20'+today.strftime('%y%m%d')
    before=(datetime.datetime.now()- relativedelta(years=2)).strftime("%Y%m%d")
    # 调用akshare的数据
    stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=code, period="daily",
                                            start_date=before, end_date=ftoday, adjust="")
    df=stock_zh_a_hist_df.loc[:,'日期':'成交量']
    df.columns = ['trade_date', 'open', 'close','high','low','vol']
    df['ma5']=df.close.rolling(window=5).mean()
    df['ma10'] = df.close.rolling(window=10).mean()
    df['ma20'] = df.close.rolling(window=20).mean()
    df['ma30'] = df.close.rolling(window=30).mean()
    print(df)
    return HttpResponse(df.to_json())
