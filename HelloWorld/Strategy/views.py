from datetime import datetime

import pandas as pd
import pymysql
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt

from . import storeHistory

from . import SmaAverages
from . import TurtleStrategy
from . import KeltnerStrategy
from . import BollStrategy
from . import MfiStrategy
from . import gruStrategy
from . import rnnStrategy
from . import lstmStrategy

from jqdatasdk import get_security_info, auth, normalize_code

auth('13951687652', 'Syj020608!')


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
    res = []
    for item in results:
        tmp = {'num': item[0], 'title': item[1], 'text': item[2], 'tag1': item[3], 'tag2': item[4], 'tag3': item[5]}
        res.append(tmp)
    # db.close()
    return HttpResponse(json.dumps(res))


@csrf_exempt
def sma(request):
    if request.headers['Content-Type'] == "application/json;charset=UTF-8":
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        backtest_id = data.get('backtest_id')
        stocks = data.get('stocks')
        startDate = data.get('startDate')
        endDate = data.get('endDate')
    else:
        username = request.POST.get("username")
        backtest_id = request.POST.get("backtest_id")
        stocks = request.POST.get("stocks")
        startDate = request.POST.get("startDate")
        endDate = request.POST.get("endDate")

    stocks = stocks.split(",")

    
    try:
        for stock in stocks:
            ncode = normalize_code(stock)  # 转成聚宽的代码
            display_name = get_security_info(ncode).display_name
    except:
        return HttpResponse(json.dumps({'code':'333'}))

    hold_result, trade_result, value_ratio, benchmark, indicator_list = SmaAverages.run_sma(stocks, startDate, endDate)
    result = storeHistory.storeStrategy(username,backtest_id,hold_result, trade_result, value_ratio, benchmark, indicator_list)
    if result == 222:
        return HttpResponse(json.dumps({'code':'222'}))

    # 数据入backtest_records库
    sql = 'INSERT INTO backtest_records (username,backtest_id,start_date,end_date,stocks) VALUES (%s,%s,%s,%s,%s)'
    cursor.execute(sql, (username, backtest_id,
                         datetime.strptime(startDate, '%Y%m%d').strftime('%Y-%m-%d'),
                         datetime.strptime(endDate, '%Y%m%d').strftime('%Y-%m-%d')
                         , ','.join(stocks)))
    db.commit()

    # 格式化，保留两位小数
    value_ratio['ratio'] = value_ratio['ratio'].map(lambda x: x * 100).apply(lambda x: format(x, '.2')).astype(float)
    value_ratio = value_ratio.to_json(orient='values')

    hold_result['price'] = hold_result['price'].apply(lambda x: format(x, '.2')).astype(float)
    hold_result['profit'] = hold_result['profit'].apply(lambda x: format(x, '.2')).astype(float)
    hold_result = hold_result.to_json(orient='values')

    trade_result['transaction'] = trade_result['transaction'].apply(lambda x: format(x, '.2')).astype("float64")
    trade_result = trade_result.to_json(orient='values')

    benchmark = benchmark.to_json(orient='values')

    return HttpResponse(json.dumps(
        {'hold_result': hold_result, 'trade_result': trade_result, 'value_ratio': value_ratio, 'benchmark': benchmark,
         'indicator_list': indicator_list}))


@csrf_exempt
def turtle(request):
    if request.headers['Content-Type'] == "application/json;charset=UTF-8":
        data = json.loads(request.body.decode('utf-8'))
        username=data.get('username')
        backtest_id=data.get('backtest_id')
        stocks = data.get('stocks')
        startDate = data.get('startDate')
        endDate = data.get('endDate')
    else:
        username= request.POST.get("username")
        backtest_id= request.POST.get("backtest_id")
        stocks = request.POST.get("stocks")
        startDate = request.POST.get("startDate")
        endDate = request.POST.get("endDate")
    stocks = stocks.split(",")

    try:
        for stock in stocks:
            ncode = normalize_code(stock)  # 转成聚宽的代码
            display_name = get_security_info(ncode).display_name
    except:
        return HttpResponse(json.dumps({'code':'333'}))# 有不存在的股票

    # 数据入backtest_records库
    sql = 'INSERT INTO backtest_records (username,backtest_id,start_date,end_date,stocks) VALUES (%s,%s,%s,%s,%s)'
    cursor.execute(sql, (username, backtest_id,
                         datetime.strptime(startDate, '%Y%m%d').strftime('%Y-%m-%d'),
                         datetime.strptime(endDate, '%Y%m%d').strftime('%Y-%m-%d')
                         ,','.join(stocks)))
    db.commit()

    hold_result, trade_result, value_ratio, benchmark, indicator_list = TurtleStrategy.run_turtle(stocks, startDate,
                                                                                                  endDate)
    result = storeHistory.storeStrategy(username,backtest_id,hold_result, trade_result, value_ratio, benchmark, indicator_list)
    if result == 222:
        return HttpResponse(json.dumps({'code':'222'}))# 回测记录名重复，请输入不同的回测名称
    # 格式化，保留两位小数
    value_ratio['ratio'] = value_ratio['ratio'].map(lambda x: x * 100).apply(lambda x: format(x, '.2')).astype(float)
    value_ratio = value_ratio.to_json(orient='values')

    hold_result['price']=hold_result['price'].apply(lambda x: format(x, '.2')).astype(float)
    hold_result['profit']=hold_result['profit'].apply(lambda x: format(x, '.2')).astype(float)
    hold_result = hold_result.to_json(orient='values')

    trade_result['transaction']=trade_result['transaction'].apply(lambda x: format(x, '.2')).astype("float64")
    trade_result = trade_result.to_json(orient='values')

    benchmark = benchmark.to_json(orient='values')

    return HttpResponse(json.dumps(
        {'hold_result': hold_result, 'trade_result': trade_result, 'value_ratio': value_ratio, 'benchmark': benchmark,
         'indicator_list': indicator_list}))


@csrf_exempt
def keltner(request):
    if request.headers['Content-Type'] == "application/json;charset=UTF-8":
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        backtest_id = data.get('backtest_id')
        stocks = data.get('stocks')
        startDate = data.get('startDate')
        endDate = data.get('endDate')
    else:
        username = request.POST.get("username")
        backtest_id = request.POST.get("backtest_id")
        stocks = request.POST.get("stocks")
        startDate = request.POST.get("startDate")
        endDate = request.POST.get("endDate")

    stocks = stocks.split(",")

    try:
        for stock in stocks:
            ncode = normalize_code(stock)  # 转成聚宽的代码
            display_name = get_security_info(ncode).display_name
    except:
        return HttpResponse(json.dumps({'code':'333'}))

    # 数据入backtest_records库
    sql = 'INSERT INTO backtest_records (username,backtest_id,start_date,end_date,stocks) VALUES (%s,%s,%s,%s,%s)'
    cursor.execute(sql, (username, backtest_id,
                         datetime.strptime(startDate, '%Y%m%d').strftime('%Y-%m-%d'),
                         datetime.strptime(endDate, '%Y%m%d').strftime('%Y-%m-%d')
                         , ','.join(stocks)))
    db.commit()

    hold_result, trade_result, value_ratio, benchmark, indicator_list = KeltnerStrategy.run_keltner(stocks, startDate,
                                                                                                    endDate)
    
    result = storeHistory.storeStrategy(username,backtest_id,hold_result, trade_result, value_ratio, benchmark, indicator_list)
    if result == 222:
        return HttpResponse(json.dumps({'code':'222'}))
    # 格式化，保留两位小数
    value_ratio['ratio'] = value_ratio['ratio'].map(lambda x: x * 100).apply(lambda x: format(x, '.2')).astype(float)
    value_ratio = value_ratio.to_json(orient='values')

    hold_result['price'] = hold_result['price'].apply(lambda x: format(x, '.2')).astype(float)
    hold_result['profit'] = hold_result['profit'].apply(lambda x: format(x, '.2')).astype(float)
    hold_result = hold_result.to_json(orient='values')

    trade_result['transaction'] = trade_result['transaction'].apply(lambda x: format(x, '.2')).astype("float64")
    trade_result = trade_result.to_json(orient='values')

    benchmark = benchmark.to_json(orient='values')

    return HttpResponse(json.dumps(
        {'hold_result': hold_result, 'trade_result': trade_result, 'value_ratio': value_ratio, 'benchmark': benchmark,
         'indicator_list': indicator_list}))


@csrf_exempt
def boll(request):
    if request.headers['Content-Type'] == "application/json;charset=UTF-8":
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        backtest_id = data.get('backtest_id')
        stocks = data.get('stocks')
        startDate = data.get('startDate')
        endDate = data.get('endDate')
    else:
        username = request.POST.get("username")
        backtest_id = request.POST.get("backtest_id")
        stocks = request.POST.get("stocks")
        startDate = request.POST.get("startDate")
        endDate = request.POST.get("endDate")

    stocks = stocks.split(",")

    try:
        for stock in stocks:
            ncode = normalize_code(stock)  # 转成聚宽的代码
            display_name = get_security_info(ncode).display_name
    except:
        return HttpResponse(json.dumps({'code':'333'}))

    # 数据入backtest_records库
    sql = 'INSERT INTO backtest_records (username,backtest_id,start_date,end_date,stocks) VALUES (%s,%s,%s,%s,%s)'
    cursor.execute(sql, (username, backtest_id,
                         datetime.strptime(startDate, '%Y%m%d').strftime('%Y-%m-%d'),
                         datetime.strptime(endDate, '%Y%m%d').strftime('%Y-%m-%d')
                         , ','.join(stocks)))
    db.commit()

    hold_result, trade_result, value_ratio, benchmark, indicator_list = BollStrategy.run_Boll(stocks, startDate,
                                                                                              endDate)

    result = storeHistory.storeStrategy(username,backtest_id,hold_result, trade_result, value_ratio, benchmark, indicator_list)
    if result == 222:
        return HttpResponse(json.dumps({'code':'222'}))
    # 格式化，保留两位小数
    value_ratio['ratio'] = value_ratio['ratio'].map(lambda x: x * 100).apply(lambda x: format(x, '.2')).astype(float)
    value_ratio = value_ratio.to_json(orient='values')

    hold_result['price'] = hold_result['price'].apply(lambda x: format(x, '.2')).astype(float)
    hold_result['profit'] = hold_result['profit'].apply(lambda x: format(x, '.2')).astype(float)
    hold_result = hold_result.to_json(orient='values')

    trade_result['transaction'] = trade_result['transaction'].apply(lambda x: format(x, '.2')).astype("float64")
    trade_result = trade_result.to_json(orient='values')

    benchmark = benchmark.to_json(orient='values')

    return HttpResponse(json.dumps(
        {'hold_result': hold_result, 'trade_result': trade_result, 'value_ratio': value_ratio, 'benchmark': benchmark,
         'indicator_list': indicator_list}))


@csrf_exempt
def mfi(request):
    if request.headers['Content-Type'] == "application/json;charset=UTF-8":
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        backtest_id = data.get('backtest_id')
        stocks = data.get('stocks')
        startDate = data.get('startDate')
        endDate = data.get('endDate')
    else:
        username = request.POST.get("username")
        backtest_id = request.POST.get("backtest_id")
        stocks = request.POST.get("stocks")
        startDate = request.POST.get("startDate")
        endDate = request.POST.get("endDate")

    stocks = stocks.split(",")

    try:
        for stock in stocks:
            ncode = normalize_code(stock)  # 转成聚宽的代码
            display_name = get_security_info(ncode).display_name
    except:
        return HttpResponse(json.dumps({'code':'333'}))

    # 数据入backtest_records库
    sql = 'INSERT INTO backtest_records (username,backtest_id,start_date,end_date,stocks) VALUES (%s,%s,%s,%s,%s)'
    cursor.execute(sql, (username, backtest_id,
                         datetime.strptime(startDate, '%Y%m%d').strftime('%Y-%m-%d'),
                         datetime.strptime(endDate, '%Y%m%d').strftime('%Y-%m-%d')
                         , ','.join(stocks)))
    db.commit()

    hold_result, trade_result, value_ratio, benchmark, indicator_list = MfiStrategy.run_mfi(stocks, startDate,
                                                                                              endDate)

    result = storeHistory.storeStrategy(username,backtest_id,hold_result, trade_result, value_ratio, benchmark, indicator_list)
    if result == 222:
        return HttpResponse(json.dumps({'code':'222'}))
    # 格式化，保留两位小数
    value_ratio['ratio'] = value_ratio['ratio'].map(lambda x: x * 100).apply(lambda x: format(x, '.2')).astype(float)
    value_ratio = value_ratio.to_json(orient='values')

    hold_result['price'] = hold_result['price'].apply(lambda x: format(x, '.2')).astype(float)
    hold_result['profit'] = hold_result['profit'].apply(lambda x: format(x, '.2')).astype(float)
    hold_result = hold_result.to_json(orient='values')

    trade_result['transaction'] = trade_result['transaction'].apply(lambda x: format(x, '.2')).astype("float64")
    trade_result = trade_result.to_json(orient='values')

    benchmark = benchmark.to_json(orient='values')

    return HttpResponse(json.dumps(
        {'hold_result': hold_result, 'trade_result': trade_result, 'value_ratio': value_ratio, 'benchmark': benchmark,
         'indicator_list': indicator_list}))


@csrf_exempt
def gru(request):
    if request.headers['Content-Type'] == "application/json;charset=UTF-8":
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        backtest_id = data.get('backtest_id')
        stocks = data.get('stocks')
        startDate = data.get('startDate')
        endDate = data.get('endDate')
        epoch = data.get('epoch')
        steps = data.get('steps')
        rate = data.get('rate')
        stock_size = data.get('stock_size')
    else:
        username = request.POST.get("username")
        backtest_id = request.POST.get("backtest_id")
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

    try:
        ncode = normalize_code(stocks)  # 转成聚宽的代码
        display_name = get_security_info(ncode).display_name
    except:
        return HttpResponse(json.dumps({'code':'333'}))

    # 数据入backtest_records库
    sql = 'INSERT INTO backtest_records (username,backtest_id,start_date,end_date,stocks) VALUES (%s,%s,%s,%s,%s)'
    cursor.execute(sql, (username, backtest_id,
                         datetime.strptime(startDate, '%Y%m%d').strftime('%Y-%m-%d'),
                         datetime.strptime(endDate, '%Y%m%d').strftime('%Y-%m-%d')
                         , stocks))
    db.commit()

    hold_result, trade_result, value_ratio, benchmark, indicator_list = gruStrategy.run_gru_final(stocks, startDate,
                                                                                                  endDate, epoch, steps,
                                                                                                  rate, stock_size)
    result = storeHistory.storeStrategy(username,backtest_id,hold_result, trade_result, value_ratio, benchmark, indicator_list)
    if result == 222:
        return HttpResponse(json.dumps({'code':'222'}))
    # 格式化，保留两位小数
    value_ratio['ratio'] = value_ratio['ratio'].map(lambda x: x * 10000).apply(lambda x: format(x, '.2')).astype(float)
    value_ratio = value_ratio.to_json(orient='values')

    hold_result['price'] = hold_result['price'].apply(lambda x: format(x, '.2')).astype(float)
    hold_result['profit'] = hold_result['profit'].apply(lambda x: format(x, '.2')).astype(float)
    hold_result = hold_result.to_json(orient='values')

    trade_result['transaction'] = trade_result['transaction'].apply(lambda x: format(x, '.2')).astype("float64")
    trade_result = trade_result.to_json(orient='values')

    benchmark = benchmark.to_json(orient='values')

    return HttpResponse(json.dumps(
        {'hold_result': hold_result, 'trade_result': trade_result, 'value_ratio': value_ratio, 'benchmark': benchmark,
         'indicator_list': indicator_list}))


@csrf_exempt
def rnn(request):
    if request.headers['Content-Type'] == "application/json;charset=UTF-8":
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        backtest_id = data.get('backtest_id')
        stocks = data.get('stocks')
        startDate = data.get('startDate')
        endDate = data.get('endDate')
        epoch = data.get('epoch')
        steps = data.get('steps')
        rate = data.get('rate')
        stock_size = data.get('stock_size')
    else:
        username = request.POST.get("username")
        backtest_id = request.POST.get("backtest_id")
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

    try:
        ncode = normalize_code(stocks)  # 转成聚宽的代码
        display_name = get_security_info(ncode).display_name
    except:
        return HttpResponse(json.dumps({'code':'333'}))

    # 数据入backtest_records库
    sql = 'INSERT INTO backtest_records (username,backtest_id,start_date,end_date,stocks) VALUES (%s,%s,%s,%s,%s)'
    cursor.execute(sql, (username, backtest_id,
                         datetime.strptime(startDate, '%Y%m%d').strftime('%Y-%m-%d'),
                         datetime.strptime(endDate, '%Y%m%d').strftime('%Y-%m-%d')
                         , stocks))
    db.commit()

    hold_result, trade_result, value_ratio, benchmark, indicator_list = rnnStrategy.run_rnn_final(stocks, startDate,
                                                                                                  endDate, epoch, steps,
                                                                                                  rate, stock_size)
    result = storeHistory.storeStrategy(username,backtest_id,hold_result, trade_result, value_ratio, benchmark, indicator_list)
    if result == 222:
        return HttpResponse(json.dumps({'code':'222'}))
    # 格式化，保留两位小数
    value_ratio['ratio'] = value_ratio['ratio'].map(lambda x: x * 10000).apply(lambda x: format(x, '.2')).astype(float)
    value_ratio = value_ratio.to_json(orient='values')

    hold_result['price'] = hold_result['price'].apply(lambda x: format(x, '.2')).astype(float)
    hold_result['profit'] = hold_result['profit'].apply(lambda x: format(x, '.2')).astype(float)
    hold_result = hold_result.to_json(orient='values')

    trade_result['transaction'] = trade_result['transaction'].apply(lambda x: format(x, '.2')).astype("float64")
    trade_result = trade_result.to_json(orient='values')

    benchmark = benchmark.to_json(orient='values')

    return HttpResponse(json.dumps(
        {'hold_result': hold_result, 'trade_result': trade_result, 'value_ratio': value_ratio, 'benchmark': benchmark,
         'indicator_list': indicator_list}))

@csrf_exempt
def lstm(request):
    if request.headers['Content-Type'] == "application/json;charset=UTF-8":
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        backtest_id = data.get('backtest_id')
        stocks = data.get('stocks')
        startDate = data.get('startDate')
        endDate = data.get('endDate')
        epoch = data.get('epoch')
        steps = data.get('steps')
        rate = data.get('rate')
        stock_size = data.get('stock_size')
    else:
        username = request.POST.get("username")
        backtest_id = request.POST.get("backtest_id")
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

    try:
        ncode = normalize_code(stocks)  # 转成聚宽的代码
        display_name = get_security_info(ncode).display_name
    except:
        return HttpResponse(json.dumps({'code':'333'}))

    # 数据入backtest_records库
    sql = 'INSERT INTO backtest_records (username,backtest_id,start_date,end_date,stocks) VALUES (%s,%s,%s,%s,%s)'
    cursor.execute(sql, (username, backtest_id,
                         datetime.strptime(startDate, '%Y%m%d').strftime('%Y-%m-%d'),
                         datetime.strptime(endDate, '%Y%m%d').strftime('%Y-%m-%d')
                         , stocks))
    db.commit()

    hold_result, trade_result, value_ratio, benchmark, indicator_list = lstmStrategy.run_lstm_final(stocks, startDate,
                                                                                                  endDate, epoch, steps,
                                                                                                  rate, stock_size)
    result = storeHistory.storeStrategy(username,backtest_id,hold_result, trade_result, value_ratio, benchmark, indicator_list)
    if result == 222:
        return HttpResponse(json.dumps({'code':'222'}))
    # 格式化，保留两位小数
    value_ratio['ratio'] = value_ratio['ratio'].map(lambda x: x * 10000).apply(lambda x: format(x, '.2')).astype(float)
    value_ratio = value_ratio.to_json(orient='values')

    hold_result['price'] = hold_result['price'].apply(lambda x: format(x, '.2')).astype(float)
    hold_result['profit'] = hold_result['profit'].apply(lambda x: format(x, '.2')).astype(float)
    hold_result = hold_result.to_json(orient='values')

    trade_result['transaction'] = trade_result['transaction'].apply(lambda x: format(x, '.2')).astype("float64")
    trade_result = trade_result.to_json(orient='values')

    benchmark = benchmark.to_json(orient='values')

    return HttpResponse(json.dumps(
        {'hold_result': hold_result, 'trade_result': trade_result, 'value_ratio': value_ratio, 'benchmark': benchmark,
         'indicator_list': indicator_list}))


@csrf_exempt
def uploadCode(request):
    # if request.headers['Content-Type'] == "application/json;charset=UTF-8":
    #     data = json.loads(request.body.decode('utf-8'))
    #     stocks = data.get('stocks')
    # else:
    #     stocks = request.POST.get("stocks")

    filename = './Strategy/UserStrategy.py'
    with open(filename,'r',errors='ignore') as f:
        code=f.read()
        # print(code)

    return HttpResponse(json.dumps({'code':code}))


@csrf_exempt
def downloadCode(request):
    if request.headers['Content-Type'] == "application/json;charset=UTF-8":
        data = json.loads(request.body.decode('utf-8'))
        # userCodeName = data.get('userCodeName')
        userCode = data.get('userCode')
    else:
        # userCodeName = request.POST.get("userCodeName")
        userCode = request.POST.get("userCode")

    # filename = './Strategy/'+userCodeName+'.py'
    filename = './Strategy/UserStrategy.py'
    with open(filename,'w') as f: # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
        f.write(userCode)
        f.close()
    
    from . import UserStrategy
    try:
        hold_result, trade_result, value_ratio, benchmark, indicator_list = UserStrategy.run_user()
    except:
        return HttpResponse(json.dumps({'code':222}))
    hold_result = hold_result.to_json(orient='records')
    trade_result = trade_result.to_json(orient='records')
    value_ratio = value_ratio.to_json(orient='records')
    benchmark = benchmark.to_json(orient='records')
    # print(indicator_list)

    return HttpResponse(json.dumps(
        {'hold_result': hold_result, 'trade_result': trade_result, 'value_ratio': value_ratio, 'benchmark': benchmark,
         'indicator_list': indicator_list}))

# 工具函数，将Mysqldb中cursor.fetchall()的结果读取为JSON
def fetch_dict_result(cur):
    row_headers = [x[0] for x in cur.description]  # this will extract row headers
    rv = cur.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    return json.dumps(json_data)

def getBacktestRecords(request):
    if request.headers['Content-Type'] == "application/json;charset=UTF-8":
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
    else:
        username = request.GET.get("username")
    sql = 'SELECT * FROM backtest_records WHERE username = %s'
    cursor.execute(sql, username)
    res = fetch_dict_result(cursor)
    db.commit()
    return HttpResponse(res)

def getSingleBacktestRecord(request):
    if request.headers['Content-Type'] == "application/json;charset=UTF-8":
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        backtest_id=data.get('backtest_id')
    else:
        username = request.GET.get("username")
        backtest_id=request.GET.get("backtest_id")
    sql = 'SELECT remain_values,str_income,multi_income,year_income_rate,max_back,max_amount,xia_rate ' \
          'FROM indicator_list WHERE username = %s and backtest_id = %s'
    cursor.execute(sql, (username,backtest_id))
    results = cursor.fetchall()
    indicator_list = results[0]
    db.commit()

    sql = 'SELECT date,code,status,size,price,transaction FROM trade_result WHERE username = %s and backtest_id = %s'
    cursor.execute(sql, (username, backtest_id))
    res = fetch_dict_result(cursor)
    trade_result = pd.DataFrame(json.loads(res)).to_json(orient="values")
    db.commit()

    sql = 'SELECT date,code,size,price,present,profit FROM hold_result WHERE username = %s and backtest_id = %s'
    cursor.execute(sql, (username, backtest_id))
    res = fetch_dict_result(cursor)
    hold_result = pd.DataFrame(json.loads(res)).to_json(orient="values")
    db.commit()

    sql = 'SELECT date,ratio FROM value_ratio WHERE username = %s and backtest_id = %s'
    cursor.execute(sql, (username, backtest_id))
    res = fetch_dict_result(cursor)
    value_ratio = pd.DataFrame(json.loads(res)).to_json(orient="values")
    db.commit()

    sql = 'SELECT date,num FROM benchmark WHERE username = %s and backtest_id = %s'
    cursor.execute(sql, (username, backtest_id))
    res = fetch_dict_result(cursor)
    benchmark = pd.DataFrame(json.loads(res)).to_json(orient="values")
    db.commit()

    return HttpResponse(json.dumps(
        {'hold_result': hold_result, 'trade_result': trade_result, 'value_ratio': value_ratio, 'benchmark': benchmark,
         'indicator_list': indicator_list}))