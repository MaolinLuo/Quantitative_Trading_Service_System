import pymysql
from django.http import HttpResponse
import json

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
    return HttpResponse(json.dumps(res))