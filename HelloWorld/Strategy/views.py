import pymysql
from django.http import HttpResponse

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
        print(item)

    return HttpResponse("Hello world!")