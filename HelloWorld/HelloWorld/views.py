import json

from django.http import HttpResponse
import pymysql
from django.views.decorators.csrf import csrf_exempt

# 120.46.205.232  Quantitative_Trading_Service_System
db = pymysql.connect(host='localhost',
                     user='root',
                     password='505505',
                     database='test')
cursor = db.cursor()

def hello(request):
    return HttpResponse("Hello world!")

@csrf_exempt
def login(request):
    if request.headers['Content-Type']=="application/json;charset=UTF-8":
        data=json.loads(request.body.decode('utf-8'))
        name=data.get('username')
        password=data.get('password')
    else:
        name = request.POST.get("username")
        password = request.POST.get("password")
    # print(name)
    # print(password)
    sql = 'SELECT * FROM user WHERE username = %s'
    cursor.execute(sql, name)
    results = cursor.fetchall()
    # print(results)
    if results:
        if results[0][1]==password:
            return HttpResponse(json.dumps({'code':'111'})) # 登录成功
        else:
            return HttpResponse(json.dumps({'code':'222'})) # 密码不对
    else:
        return HttpResponse(json.dumps({'code':'333'})) # 用户名不存在

@csrf_exempt
def register(request):
    if request.headers['Content-Type'] == "application/json;charset=UTF-8":
        data = json.loads(request.body.decode('utf-8'))
        name = data.get('username')
        password = data.get('password')
    else:
        name = request.POST.get("username")
        password = request.POST.get("password")
    sql = 'SELECT * FROM user WHERE username = %s'
    cursor.execute(sql, name)
    results = cursor.fetchall()
    # print(results)
    if results:
        return HttpResponse(json.dumps({'code':'222'})) # 用户名已存在
    else:
        sql='INSERT INTO user (username,password,isAdmin) VALUES (%s,%s,0)'
        cursor.execute(sql,(name,password))
        db.commit()
        return HttpResponse(json.dumps({'code':'111'})) # 注册成功
