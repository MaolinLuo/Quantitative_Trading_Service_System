<template>
<div class="bottom-link">
<div id="footer">
  <div class="wp19 fleft">
    <div class="title">数据源</div>
    <div ><a href="https://www.akshare.xyz/">akshare</a></div>
    <div><a href="https://www.joinquant.com/">聚宽</a></div>
    <div><a href="https://tushare.pro/">tushare</a></div>
  </div>
  <div class="wp19 fleft">
    <div class="title">帮助文档</div>
    <div ><a href="https://www.runoob.com/python/python-tutorial.html">python教程</a></div>
    <div><a href="https://www.runoob.com/pandas/pandas-tutorial.html">Pandas教程</a></div>
    <div><a href="https://pytorch.org/">Pytorch教程</a></div>
  </div>
  <div class="wp19 fleft">
    <div class="title">财经频道</div>
    <div ><a href="https://xueqiu.com/u/8287840120">雪球</a></div>
    <div><a href="https://www.eastmoney.com/">东方财富</a></div>
    <div><a href="https://www.10jqka.com.cn/">同花顺</a></div>
  </div>
  <div class="wp19 fleft" style="margin-bottom:10px">
    <div class="title">量化投资</div>
    <div ><a href="https://www.joinquant.com/">聚宽</a></div>
    <div><a href="https://bigquant.com/wiki/home">BigQuant</a></div>
    <div><a href="https://backtrader.apachecn.org/#/">Backtrader</a></div>
  </div>
</div>
</div>
</template>

<script>
export default {
  name: "FooterBar"
}
</script>

<style scoped>
.title {
  color: #b9bbbe;
  font-size: 18px;
  padding-bottom: 10px;
}
.fleft {
  float: left;
}

.wp19 {
  width: 19%;
}
#footer .c333 {
  line-height: 35px;
}
/* #footer p {
  margin: 0;
  color: #777;
} */
#footer {
  display: flex;
  flex-direction: row;
  padding-top: 20px;
  text-align: center;
  width: 100%;
  font: 12px/24px \5b8b\4f53, tahoma, arial, sans-serif;
  justify-content: center;
}
.bottom-link {
  width: 100%;
  background-color:#212529;
}
a{
  color: white;
  text-decoration: none;
  text-align: center;
}
</style>