from django.http import HttpResponse
from django.shortcuts import render
import pymysql
from django.views.decorators.csrf import csrf_exempt

db = pymysql.connect(host='120.46.152.35',
                     user='root',
                     password='123456',
                     database='Quantitative_Trading_Service_System')
cursor = db.cursor()


# from HelloWorld.TestModel.models import stocks_basicinfo

# def hello(request):
#     return HttpResponse("Hello world!")
#
# def runoob(request):
#   views_dict = {"name":"菜鸟教程"}
#   return  render(request,"runoob.html", {"views_dict":views_dict})
#
# def rb1(request):
#     name = request.GET.get("name")
#     # 数据库操作
#     # test1=stocks_basicinfo(ts_code='123456')
#     # test1.save()
#     return HttpResponse('姓名：{}'.format(name))
#     # return HttpResponse("<p>数据添加成功！</p>")
#
# #在处理函数加此装饰器即可
# @csrf_exempt
# def rb2(request):
#     name = request.POST.get("name")
#     return HttpResponse('姓名：{}'.format(name))
@csrf_exempt
def login(request):
    name = request.POST.get("username")
    password = request.POST.get("password")
    sql = 'SELECT * FROM user WHERE username = %s'
    cursor.execute(sql, name)
    results = cursor.fetchall()
    print(results)
    if results:
        if results[0][1]==password:
            return HttpResponse("111") # 登录成功
        else:
            return HttpResponse("222") # 密码不对
    else:
        return HttpResponse("333") # 用户名不存在
