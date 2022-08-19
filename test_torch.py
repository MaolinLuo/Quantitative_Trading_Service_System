# import akshare as ak
#
# stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol="000001", period="daily", start_date="20130601", end_date='20220601', adjust="")
# df=stock_zh_a_hist_df.loc[:,'日期':'收盘']
# df.columns=['Date','Open','Close']
# print(df)

import akshare as ak

stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol="000001", period="daily", start_date="20170301", end_date='20210907', adjust="")
print(stock_zh_a_hist_df)