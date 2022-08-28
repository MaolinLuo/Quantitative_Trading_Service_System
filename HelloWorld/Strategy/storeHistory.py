import pymysql

db = pymysql.connect(host='localhost',
                     user='root',
                     password='505505',
                     database='test')
cursor = db.cursor()

def storeStrategy(username, backtest_id, hold_result, trade_result, value_ratio, benchmark, indicator_list):
    
    for id_x, row in hold_result.iterrows():
        date = row[0]
        code = row[1]
        size = row[2]
        price = row[3]
        present = row[4]
        profit = row[5]
        sql='INSERT INTO hold_result (username,backtest_id,date,code,size,price,present,profit) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(sql,(username,backtest_id,date,code,size,price,present,profit))
        db.commit()
    
    for id_x, row in trade_result.iterrows():
        date = row[0]
        code = row[1]
        status = row[2]
        size = row[3]
        price = row[4]
        transaction = row[5]
        sql='INSERT INTO trade_result (username,backtest_id,date,code,status,size,price,transaction) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(sql,(username,backtest_id,date,code,status,size,price,transaction))
        db.commit()


    for id_x, row in value_ratio.iterrows():
        date = row[0]
        ratio = row[1]
        sql='INSERT INTO value_ratio (username,backtest_id,date,ratio) VALUES (%s,%s,%s,%s)'
        cursor.execute(sql,(username,backtest_id,date,ratio))
        db.commit()

    for id_x, row in benchmark.iterrows():
        date = row[0]
        QuoteChange = row[1]
        sql='INSERT INTO benchmark (username,backtest_id,date,num) VALUES (%s,%s,%s,%s)'
        cursor.execute(sql,(username,backtest_id,date,QuoteChange))
        db.commit()


    remain_values = indicator_list[0]
    str_income = indicator_list[1]
    multi_income = indicator_list[2]
    year_income_rate = indicator_list[3]
    max_back = indicator_list[4]
    max_amount = indicator_list[5]
    xia_rate = indicator_list[6]
    sql='INSERT INTO indicator_list (username,backtest_id,remain_values,str_income,multi_income,year_income_rate,max_back,max_amount,xia_rate) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    cursor.execute(sql,(username,backtest_id,remain_values,str_income,multi_income,year_income_rate,max_back,max_amount,xia_rate))
    db.commit()
