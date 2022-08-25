import json
from django.http import HttpResponse
import pymysql

# 120.46.205.232  Quantitative_Trading_Service_System quantitative_trading_service_system
db = pymysql.connect(host='localhost',
                     user='root',
                     password='505505',
                     database='test')
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
    res = fetch_dict_result(cursor)
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


