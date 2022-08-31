import json
from django.http import HttpResponse
import pymysql
from django.views.decorators.csrf import csrf_exempt
import hashlib
import jwt
import time

# 生成一个字典，包含我们的具体信息
d = {
    # 公共声明
    'exp': time.time() + 3000,  # (Expiration Time) 此token的过期时间的时间戳
    'iat': time.time(),  # (Issued At) 指明此创建时间的时间戳
    'iss': 'Issuer',  # (Issuer) 指明此token的签发者

    # 私有声明
    'data': {
        'username': 'xjj',
        'timestamp': time.time()
    }
}

# 120.46.205.232  Quantitative_Trading_Service_System quantitative_trading_service_system
db = pymysql.connect(host='localhost',
                     user='root',
                     password='123456',
                     database='quantitative_trading_service_system')
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
    sql = 'SELECT * FROM user WHERE username = %s'
    cursor.execute(sql, name)
    results = cursor.fetchall()
    Encry = hashlib.md5()  # 实例化md5
    Encry.update(password.encode())  # 字符串字节加密
    pwd = Encry.hexdigest()  # 字符串加密
    if results:
        if results[0][1]==pwd:
            token = jwt.encode(d, pwd, algorithm='HS256')
            return HttpResponse(json.dumps({'code':'111','userType':results[0][2],'token':str(token)})) # 登录成功
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
        sql='INSERT INTO user (username,password,userType) VALUES (%s,%s,0)'
        Encry = hashlib.md5()  # 实例化md5
        Encry.update(password.encode())  # 字符串字节加密
        md5_pwd = Encry.hexdigest()  # 字符串加密
        cursor.execute(sql,(name,md5_pwd))
        db.commit()
        return HttpResponse(json.dumps({'code':'111'})) # 注册成功

@csrf_exempt
def toVip(request):
    if request.headers['Content-Type']=="application/json;charset=UTF-8":
        data=json.loads(request.body.decode('utf-8'))
        name=data.get('username')
    else:
        name = request.POST.get("username")
    sql = 'UPDATE user SET userType=1 WHERE username = %s'
    cursor.execute(sql, name)
    # results = cursor.fetchall()
    db.commit()
    return HttpResponse(json.dumps({'code':"111"}))
