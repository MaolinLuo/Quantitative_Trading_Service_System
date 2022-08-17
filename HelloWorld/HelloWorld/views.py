from django.http import HttpResponse
from django.shortcuts import render
import pymysql
from django.views.decorators.csrf import csrf_exempt

# 120.46.205.232  Quantitative_Trading_Service_System
db = pymysql.connect(host='120.46.205.232',
                     user='root',
                     password='123456',
                     database='quantitative_trading_service_system')
cursor = db.cursor()

def hello(request):
    return HttpResponse("Hello world!")

@csrf_exempt
def login(request):
    name = request.POST.get("username")
    password = request.POST.get("password")
    sql = 'SELECT * FROM user WHERE username = %s'
    cursor.execute(sql, name)
    results = cursor.fetchall()
    # print(results)
    if results:
        if results[0][1]==password:
            return HttpResponse("111") # 登录成功
        else:
            return HttpResponse("222") # 密码不对
    else:
        return HttpResponse("333") # 用户名不存在

@csrf_exempt
def register(request):
    name = request.POST.get("username")
    password = request.POST.get("password")
    sql = 'SELECT * FROM user WHERE username = %s'
    cursor.execute(sql, name)
    results = cursor.fetchall()
    # print(results)
    if results:
        return HttpResponse("222") # 用户名已存在
    else:
        sql='INSERT INTO user (usename,password,isAdmin) VALUES (?,?,?)'
        cursor.execute(sql,(name,password,0))
        return HttpResponse("111") # 注册成功
