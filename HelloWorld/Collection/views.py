import json
from django.http import HttpResponse
import pymysql
from jqdatasdk import *
from itertools import chain
import akshare as ak

auth('13383909875', '13383909875Zc')

# 120.46.205.232  Quantitative_Trading_Service_System quantitative_trading_service_system
db = pymysql.connect(host='localhost',
                     user='root',
                     password='123456',
                     database='quantitative_trading_service_system')
cursor = db.cursor()

# 增
def collection(request):
    if request.headers['Content-Type']=="application/json;charset=UTF-8":
        data=json.loads(request.body.decode('utf-8'))
        code=data.get('code')
        username=data.get('username')
        name=data.get('name')
    else:
        code = request.GET.get("code")
        username = request.GET.get('username')
        name = request.GET.get('name')
    sql = 'SELECT * FROM collection_list WHERE username = %s and code = %s and name = %s'
    cursor.execute(sql, (username,code,name))
    results = cursor.fetchall()
    # print(results)
    if results:# 收藏了该股票，将要删除记录
        return HttpResponse(json.dumps({'code':'222'}))  # 您已收藏该股票！
    else:# 未收藏该股票，将要增加记录
        sql = 'INSERT INTO collection_list (username,code,name) VALUES (%s,%s,%s)'
        cursor.execute(sql, (username, code,name))
        db.commit()
        return HttpResponse(json.dumps({'code':'111'})) # 成功添加到我的收藏

# 工具函数，将Mysqldb中cursor.fetchall()的结果读取为JSON
def fetch_dict_result(cur):
    row_headers = [x[0] for x in cur.description]  # this will extract row headers
    rv = cur.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    return json.dumps(json_data)

# 查
def list(request):
    if request.headers['Content-Type']=="application/json;charset=UTF-8":
        data=json.loads(request.body.decode('utf-8'))
        username=data.get('username')
    else:
        username = request.GET.get('username')
    sql = 'SELECT * FROM collection_list WHERE username = %s'
    cursor.execute(sql, username)
    # results = cursor.fetchall()
    # resultlist = list(chain.from_iterable(results))
    res = fetch_dict_result(cursor)
    # print(resultlist)
    ###########################
    # ncode = normalize_code(code)  # 转成聚宽的代码
    # try:
    #     display_name = get_security_info(ncode).display_name
    # except:
    #     return HttpResponse(json.dumps({'code': '222'}))
    # df = ak.stock_zh_a_spot_em()
    # df = df.loc[df['代码'] == code]
    # df = df.loc[:, ('最新价', '今开', '涨跌额', '最高', '涨跌幅', '名称')]
    # res = []
    # res.append({"最新价": df.iat[0, 0], "开盘价": df.iat[0, 1], "涨跌": df.iat[0, 2], "最高价": df.iat[0, 3],
    #             "涨跌幅": str(df.iat[0, 4]) + '%', "名称": df.iat[0, 5]})
    # return HttpResponse(json.dumps(res))
    ###########################
    return HttpResponse(res)

# 删
def removeColl(request):
    if request.headers['Content-Type']=="application/json;charset=UTF-8":
        data=json.loads(request.body.decode('utf-8'))
        code=data.get('code')
        username=data.get('username')
    else:
        code = request.GET.get("code")
        username = request.GET.get('username')
    sql = 'SELECT * FROM collection_list WHERE username = %s and code = %s'
    cursor.execute(sql, (username, code))
    results = cursor.fetchall()
    if results:
        sql= 'DELETE FROM collection_list WHERE username = %s and code = %s'
        cursor.execute(sql, (username, code))
        db.commit()
        return HttpResponse(json.dumps({'code': '111'}))  # 成功删除
    else:
        return HttpResponse(json.dumps({'code':'222'})) # 未查询到收藏记录，删除失败


