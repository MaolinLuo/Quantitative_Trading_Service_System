import pymysql

db = pymysql.connect(host='localhost',
                     user='root',
                     password='505505',
                     database='test')
cursor = db.cursor()

def storeStrategy(username, backtest_id, hold_result, trade_result, value_ratio, benchmark, indicator_list):
    # 对于每一行，通过列名name访问对应的元素
    for id_x, row in benchmark.iterrows():
        date = row[0]
        QuoteChange = row[1]
        sql='INSERT INTO benchmark (username,backtest_id,date,num) VALUES (%s,%s,%s,%s)'
        cursor.execute(sql,(username,backtest_id,date,QuoteChange))
        db.commit()
    return 