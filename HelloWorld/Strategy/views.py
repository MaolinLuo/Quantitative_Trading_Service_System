import pymysql
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt

from . import SmaAverages


db = pymysql.connect(host='localhost',
                     user='root',
                     password='123456',
                     database='quantitative_trading_service_system')
cursor = db.cursor()

def hello(request):
    return HttpResponse("Hello world!")

def list(request):
    sql = 'SELECT * FROM strategy'
    cursor.execute(sql)
    results = cursor.fetchall()
    res=[]
    for item in results:
        tmp={'num':item[0],'title':item[1],'text':item[2],'tag1':item[3],'tag2':item[4],'tag3':item[5]}
        res.append(tmp)
    db.close()
    return HttpResponse(json.dumps(res))

@csrf_exempt
def sma(request):
    if request.headers['Content-Type']=="application/json;charset=UTF-8":
        data=json.loads(request.body.decode('utf-8'))
        stocks=data.get('stocks')
        startDate=data.get('startDate')
        endDate=data.get('endDate')
    else:
        stocks = request.POST.get("stocks")
        startDate = request.POST.get("startDate")
        endDate = request.POST.get("endDate")

    stocks = stocks.split(",")
    hold_result, trade_result, value_ratio, indicator_list = SmaAverages.run_sma(stocks, startDate, endDate)
    hold_result = hold_result.to_json(orient = 'records')
    trade_result = trade_result.to_json(orient = 'records')
    value_ratio = value_ratio.to_json(orient = 'records')
    res=[]
    res.append(hold_result)
    res.append(trade_result)
    res.append(value_ratio)
    res.append(indicator_list)
    return HttpResponse(res)

@csrf_exempt
def turtle(request):
    if request.headers['Content-Type']=="application/json;charset=UTF-8":
        data=json.loads(request.body.decode('utf-8'))
        stocks=data.get('stocks')
        startDate=data.get('startDate')
        endDate=data.get('endDate')
    else:
        stocks = request.POST.get("stocks")
        startDate = request.POST.get("startDate")
        endDate = request.POST.get("endDate")

    stocks = stocks.split(",")
    hold_result, trade_result, value_ratio, indicator_list = SmaAverages.run_sma(stocks, startDate, endDate)
    hold_result = hold_result.to_json(orient = 'records')
    trade_result = trade_result.to_json(orient = 'records')
    value_ratio = value_ratio.to_json(orient = 'records')
    
    return HttpResponse(json.dumps({'hold_result':hold_result,'trade_result':trade_result,'value_ratio':value_ratio,'indicator_list':indicator_list})) 
