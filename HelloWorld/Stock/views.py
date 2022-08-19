import json
from dateutil.relativedelta import relativedelta
from django.http import HttpResponse
import akshare as ak
import datetime
import akshare as ak

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

def allStocks(request):
    if request.headers['Content-Type']=="application/json;charset=UTF-8":
        data=json.loads(request.body.decode('utf-8'))
        pagenum=data.get('pagenum')
    else:
        pagenum = request.GET.get("pagenum")
    # 调用akshare的数据
    stock_zh_a_spot_em_df = ak.stock_zh_a_spot_em()
    df=stock_zh_a_spot_em_df.loc[:,'序号':'成交量']
    df.columns = ['num', 'code', 'name','price','range','amount','vol']
    df=df.iloc[int(pagenum)*50:int(pagenum)*50+50]
    i=0
    res=[]
    while i<50:
        tmp={"number":str(df.iat[i,0]),"code":str(df.iat[i,1]),"stock_name":df.iat[i,2],"present_price":str(df.iat[i,3]),
             "change_percent":str(df.iat[i,4]),"change_volume":str(df.iat[i,5]),"trade_volume":str(df.iat[i,6])}
        res.append(tmp)
        i+=1
    return HttpResponse(json.dumps(res))