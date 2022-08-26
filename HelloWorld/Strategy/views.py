import pymysql
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt

from . import SmaAverages
from . import TurtleStrategy
from . import KeltnerStrategy
from . import BollStrategy
from . import gruStrategy
from . import rnnStrategy

db = pymysql.connect(host='localhost',
                     user='root',
                     password='505505',
                     database='test')
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
    hold_result, trade_result, value_ratio, benchmark, indicator_list = SmaAverages.run_sma(stocks, startDate, endDate)
    hold_result = hold_result.to_json(orient = 'records')
    trade_result = trade_result.to_json(orient = 'records')
    value_ratio = value_ratio.to_json(orient = 'records')
    benchmark = benchmark.to_json(orient='records')
    
    return HttpResponse(json.dumps({'hold_result':hold_result,'trade_result':trade_result,'value_ratio':value_ratio,'benchmark':benchmark,'indicator_list':indicator_list})) 

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
    hold_result, trade_result, value_ratio, benchmark, indicator_list = TurtleStrategy.run_turtle(stocks, startDate, endDate)
    hold_result = hold_result.to_json(orient = 'records')
    trade_result = trade_result.to_json(orient = 'records')
    value_ratio = value_ratio.to_json(orient = 'records')
    benchmark = benchmark.to_json(orient='records')
    
    return HttpResponse(json.dumps({'hold_result':hold_result,'trade_result':trade_result,'value_ratio':value_ratio,'benchmark':benchmark,'indicator_list':indicator_list})) 


@csrf_exempt
def keltner(request):
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
    hold_result, trade_result, value_ratio, benchmark, indicator_list = KeltnerStrategy.run_keltner(stocks, startDate, endDate)
    hold_result = hold_result.to_json(orient = 'records')
    trade_result = trade_result.to_json(orient = 'records')
    value_ratio = value_ratio.to_json(orient = 'records')
    benchmark = benchmark.to_json(orient = 'records')
    
    return HttpResponse(json.dumps({'hold_result':hold_result,'trade_result':trade_result,'value_ratio':value_ratio,'benchmark':benchmark, 'indicator_list':indicator_list})) 

@csrf_exempt
def boll(request):
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
    hold_result, trade_result, value_ratio, benchmark, indicator_list = BollStrategy.run_Boll(stocks, startDate, endDate)
    hold_result = hold_result.to_json(orient = 'records')
    trade_result = trade_result.to_json(orient = 'records')
    value_ratio = value_ratio.to_json(orient = 'records')
    benchmark = benchmark.to_json(orient = 'records')

    return HttpResponse(json.dumps({'hold_result':hold_result,'trade_result':trade_result,'value_ratio':value_ratio,'benchmark':benchmark, 'indicator_list':indicator_list})) 



@csrf_exempt
def gru(request):
    if request.headers['Content-Type']=="application/json;charset=UTF-8":
        data=json.loads(request.body.decode('utf-8'))
        stocks=data.get('stocks')
        startDate=data.get('startDate')
        endDate=data.get('endDate')
        epoch=data.get('epoch')
        steps=data.get('steps')
        rate=data.get('rate')
        stock_size=data.get('stock_size')
    else:
        stocks = request.POST.get("stocks")
        startDate = request.POST.get("startDate")
        endDate = request.POST.get("endDate")
        epoch = request.POST.get("epoch")
        steps = request.POST.get("steps")
        rate = request.POST.get("rate")
        stock_size = request.POST.get("stock_size")


    epoch = int(epoch)
    steps = int(steps)
    rate = float(rate)
    stock_size = int(stock_size)
    hold_result, trade_result, value_ratio, benchmark, indicator_list = gruStrategy.run_gru_final(stocks, startDate, endDate,epoch,steps,rate,stock_size)
    hold_result = hold_result.to_json(orient = 'records')
    trade_result = trade_result.to_json(orient = 'records')
    value_ratio = value_ratio.to_json(orient = 'records')
    benchmark = benchmark.to_json(orient = 'records')
    
    return HttpResponse(json.dumps({'hold_result':hold_result,'trade_result':trade_result,'value_ratio':value_ratio,'benchmark':benchmark, 'indicator_list':indicator_list})) 


@csrf_exempt
def rnn(request):
    if request.headers['Content-Type']=="application/json;charset=UTF-8":
        data=json.loads(request.body.decode('utf-8'))
        stocks=data.get('stocks')
        startDate=data.get('startDate')
        endDate=data.get('endDate')
        epoch=data.get('epoch')
        steps=data.get('steps')
        rate=data.get('rate')
        stock_size=data.get('stock_size')
    else:
        stocks = request.POST.get("stocks")
        startDate = request.POST.get("startDate")
        endDate = request.POST.get("endDate")
        epoch = request.POST.get("epoch")
        steps = request.POST.get("steps")
        rate = request.POST.get("rate")
        stock_size = request.POST.get("stock_size")


    epoch = int(epoch)
    steps = int(steps)
    rate = float(rate)
    stock_size = int(stock_size)
    hold_result, trade_result, value_ratio, benchmark, indicator_list = gruStrategy.run_gru_final(stocks, startDate, endDate,epoch,steps,rate,stock_size)
    hold_result = hold_result.to_json(orient = 'records')
    trade_result = trade_result.to_json(orient = 'records')
    value_ratio = value_ratio.to_json(orient = 'records')
    benchmark = benchmark.to_json(orient = 'records')
    
    return HttpResponse(json.dumps({'hold_result':hold_result,'trade_result':trade_result,'value_ratio':value_ratio,'benchmark':benchmark, 'indicator_list':indicator_list})) 
