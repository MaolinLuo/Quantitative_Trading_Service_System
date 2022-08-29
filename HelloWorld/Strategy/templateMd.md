## 《如何使用SeuQuant自定义策略》
## 一.SeuQuant的依赖
   1. 基本框架:backtrader回测框架
   2. 数据分析:pandas
   3. 数据拉取与处理回测结果:SeuQuant团队编写的util包,对backtrader做了一定的封装
   4. 模板已导入依赖包

          from . import util 
          import backtrader as bt
          import pandas as pd 
   5. 可以自行导入想用的包
   6. 目前暂不支持自定义机器学习策略
 
## 二.策略启动函数
  1. 启动函数

          def run_user(ts_code_list=['000001.SZ','000002.SZ'],startdate='20220419',enddate='20220821'):
   其中函数名不能修改，用户可以修改函数参数
  ts_code_list(回测股票列表),startdate(回测开始日期),enddate(回测结束日期),
  #### <font color=Red size=3px>参数如上图格式,其中回测结束日期不要设置为今天以后,回测开始日期最早可至20150101</font>
  #### <font color=Red size=3px>股票代码一定是"xxxxxx.交易所简称",SZ为深圳交易所,SH为上海交易所</font>
   ---
   2. 函数主体:
   #### <font color=black size=3px>用户只可以修改以下代码中的函数参数(UserStrategy),也可以选择不改，默认使用我们提供的类名:</font>
        cerebro.addstrategy(UserStrategy)
   #### <font color=Red size=3px>参数一定要与上面定义的策略类名一致!!!</font>
## 三、策略主体
   1. 定义策略: 
          ```class UserStrategy(bt.Strategy):```
   #### <font color=Red size=3px>可以修改类名，但在启动函数的addStrategy中一定要与定义的策略类名保持一致!!</font>
   2. 不需要修改的类方法:
       ```def log(self, txt, dt=None):```
       ```def notify_order(self, order):```
       ```def notify_trade(self, trade):```
   3. init方法(用户自定义策略需要编辑的地方):
                                  
          def init(self):
            # 用于保存订单
            self.order = None
            # 订单价格
            self.buyprice = None
             # 订单佣金
             self.buycomm = None
        用于初始化需要在策略里用到的指标,这三个指标不能删除，必须保留
        下面例子为如何初始化指标:

             # 字典形式保存
             self.sma10=dict()
             self.sma30=dict() 
             # 遍历所有股票,存储格式:{股票名:sma10}   
           for data in self.datas:
            # 计算10日均线

            self.sma10[data._name] = util.btind.MovingAverageSimple(data.close, period=self.params.period_sma10)
           # 计算30日均线
            self.sma30[data._name] = util.btind.MovingAverageSimple(data.close, period=self.params.period_sma30)
4. next函数(买卖逻辑实现函数):

    ```模板中带essential注释的代码不要删!!!!```
   如何买与卖:
    
         # 遍历回测股票组合
         for data in self.datas:
            #获取持仓
            pos = self.getposition(data)
            # 持仓大于0才能卖,如果要做空单则不要加
            if pos.size>0:
              if(卖出信号):
                 self.order=self.sell(data=data,size=卖出数量)
            else 
              if(买入信号):
                 self.order=self.sell(data=data,size=买入数量)
5. 更多操作请访问[backtrader官方文档](https://www.backtrader.com/)|[中文文档](https://backtrader.apachecn.org/#/)



        

        

          
    

     

