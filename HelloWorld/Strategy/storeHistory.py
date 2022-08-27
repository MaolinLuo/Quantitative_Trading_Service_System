import pymysql

db = pymysql.connect(host='localhost',
                     user='root',
                     password='505505',
                     database='test')
cursor = db.cursor()

def storeStrategy(hold_result, trade_result, value_ratio, benchmark, indicator_list):
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