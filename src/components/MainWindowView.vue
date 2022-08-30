<template>
  <div class="MainWindow" style="width:100%">
    <!-- <TopNavigator></TopNavigator> -->
    <div class="head">
      <h2>沪深市场</h2>
    </div>
    <!--大盘数据-->
    <div class="echartstable" style="height: 400px">
      <!-- 大盘数据左侧卡片选择 -->
      <div class="left">
        <div class="UpDown" @click="change(0)" :class="{newStyle:0===number}">
          <div class="image">
            <img src="../assets/ZDFB.png" style="width:25px;" />
            <h3
              style="font-size:18px;margin:0px 0px 0px 4px;
                font-weight: 700;"
            >涨跌分布</h3>
          </div>
          <p class="detail">
            <span class="c-rise" style="color:red">上涨：{{down1}} 只</span>
            <span class="c-fall" style="color:green">下跌：{{up1}} 只</span>
          </p>
        </div>
        <div class="UpDown" @click="change(1)" :class="{newStyle:1===number}">
          <div class="image" style="margin:40px 0px 0px 0px;">
            <img src="../assets/涨跌.png" style="width:40px;" />
            <div
              style="font-size:18px;margin:0px 0px 0px -3px;
                font-weight: 700;"
            >龙虎榜</div>
          </div>
        </div>
        <div class="UpDown" @click="change(2)" :class="{newStyle:2===number}">
          <div class="image" style="margin:50px 0px 0px 0px">
            <img src="../assets/钱.png" style="width:25px;" />
            <div
              style="font-size:18px;margin:0px 0px 0px 4px;
                font-weight: 700;"
            >上证指数 深证指数 创业板指</div>
          </div>
          <p class="detail"></p>
          <p class="detail">
            <!-- <span class="c-benefit" style="color:red">今日收益：10</span> -->
          </p>
        </div>
      </div>
      <!-- 大盘数据右侧图表切换区 -->
      <div class="manyCharts">
        <div class="echart" id="mychart0" style="height:100%;width:100%" v-show="number===0"></div>
        <div class="echart" id="mychart1" style="height:100%;width:100%" v-show="number===1">
          <el-table
            :data="hotData"
            height="392"
            :header-cell-style="headClass"
            :cell-style="rowClass"
            v-loading="loadingMarketTop"
            element-loading-text="拼命加载中"
          >
            <el-table-column prop="股票代码" label="股票代码"></el-table-column>
            <el-table-column prop="股票简称" label="股票简称"></el-table-column>
            <el-table-column prop="关注" label="关注"></el-table-column>
            <el-table-column prop="最新价" label="最新价"></el-table-column>
          </el-table>
        </div>
        <div class="echart" id="mychart2" style="height:100%;width:100%" v-show="number===2"></div>
      </div>
    </div>
    <!--实时指数-->
    <div class="head">
      <h2 style="border-left: 6px solid green;">实时指数</h2>
    </div>
    <div class="exponent">
      <div class="myExponent">
        <div
          class="titleEx"
          style="font-size:24px;font-weight: 700;display:flex;flex-direction:column;text-align:center"
        >
          上证指数
          <img src="../assets/上证.png" style="width:180px;margin:-3px 0px 0px px;" />
        </div>
        <div class="beauty" ref="ShangDiv">
          <div id="ShangExponent">最新价:{{Shang.ShangEx}}</div>
          <div id="ShangExponent">涨跌幅:{{Shang.ShangExPer}}%</div>
          <div id="ShangExponent">涨跌额:{{Shang.ShangExNum}}</div>
        </div>
      </div>
      <div class="myExponent">
        <div
          class="titleEx"
          style="font-size:24px;font-weight: 700;display:flex;flex-direction:column;text-align:center"
        >
          深证指数
          <img src="../assets/SZ.png" style="width:150px;margin:-20px 0px 0px 40px;" />
        </div>
        <div class="beauty">
          <div id="ShenExponent">最新价:{{Shen.ShenEx}}</div>
          <div id="ShenExponent">涨跌幅:{{Shen.ShenExPer}}%</div>
          <div id="ShenExponent">涨跌额:{{Shen.ShenExNum}}</div>
        </div>
      </div>
      <div class="myExponent" id="box">
        <div class="titleEx" style="font-size:24px;font-weight: 700;margin:0px 0px 20px 0px">创业板指</div>
        <div class="beauty">
          <div id="ChuanExponent">最新价:{{Chuan.ChuanEx}}</div>
          <div id="ChuanExponent">涨跌幅:{{Chuan.ChuanExPer}}%</div>
          <div id="ChuanExponent">涨跌额:{{Chuan.ChuanExNum}}</div>
        </div>
      </div>
    </div>
    <!--个股行情列表-->
    <div class="head">
      <div class="head">
        <h2 style="border-left: 6px solid red;">个股行情
          <a href="/userinterface" style="color:black;text-decoration:none;margin-left:20px;padding-left:10px; line-height: 21px;font-weight: 700;border-left: 8px solid  #ffef5e;padding-left: 10px;font-size: 18px;text-shadow: 0px 1px 2px #ffffff, -2px -3px 1px rgb(204, 200, 200);"> 我的收藏</a>


        </h2>



      </div>
      <div class="box">
        <el-table
          :data="tableData"
          style="width: 100%;"
          :header-cell-style="headClass"
          :cell-style="rowClass"
          v-loading="loadingStockTable"
          element-loading-text="拼命加载中"
        >
          <el-table-column prop="number" label="序号" width="50"></el-table-column>
          <el-table-column prop="code" label="代码">
            <template slot-scope="scope">
              <a
                target="_blank"
                class="buttonText"
                @click="toStock(scope.row.code,scope.row.stock_name)"
              >{{scope.row.code}}</a>
            </template>
          </el-table-column>
          <el-table-column prop="stock_name" label="名称">
            <template slot-scope="scope">
              <a
                target="_blank"
                class="buttonText"
                @click="toCompany(scope.row.code,scope.row.stock_name)"
              >{{scope.row.stock_name}}</a>
            </template>
          </el-table-column>
          <el-table-column prop="present_price" label="最新价" style="olor:red"></el-table-column>
          <el-table-column prop="change_percent" label="涨跌幅">
            <template scope="scope">
              <span
                v-if="scope.row.change_percent>=0"
                style="color:red"
              >{{ scope.row.change_percent}}</span>
              <span v-else style="color:green">{{ scope.row.change_percent}}</span>
            </template>
          </el-table-column>
          <el-table-column prop="change_volume" label="涨跌额">
            <template scope="scope">
              <span v-if="scope.row.change_volume>=0" style="color:red">{{ scope.row.change_volume}}</span>
              <span v-else style="color:green">{{ scope.row.change_volume}}</span>
            </template>
          </el-table-column>
          <el-table-column prop="trade_volume" label="成交量"></el-table-column>
          <el-table-column prop="trade_price" label="成交额"></el-table-column>
          <el-table-column prop="violate" label="振幅"></el-table-column>
          <el-table-column prop="high" label="最高"></el-table-column>
          <el-table-column prop="low" label="最低"></el-table-column>
          <el-table-column prop="today_open" label="今开"></el-table-column>
          <el-table-column prop="yesterday_close" label="昨收"></el-table-column>
          <el-table-column prop="rate" label="量比"></el-table-column>
          <el-table-column prop="change_rate" label="换手率"></el-table-column>
          <el-table-column prop="collect" label="收藏">
            <template scope="scope">
              <img
                src="../assets/plus_logo.png"
                @click="addCollect(scope.row.stock_name,scope.row.code)"
              />
            </template>
          </el-table-column>
        </el-table>
        <el-pagination
          layout="prev, pager, next"
          :total="total"
          :current-page.sync="pageNo"
          :page-size="limit"
          @current-change="handleCurrentChange"
        ></el-pagination>
      </div>
    </div>
  </div>
</template>
<script>
import { Loading } from "element-ui";
import request from "@/util/request";
import * as echarts from "echarts";
export default {
  data() {
    return {
      // el-ui加载动画显示判断
      loadingMarketTop: true,
      loadingStockTable: true,
      // 实时指数数据
      Shang: { ShangEx: 0, ShangExPer: 0, ShangExNum: 0 },
      Shen: { ShenEx: 0, ShenExPer: 0, ShenExNum: 0 },
      Chuan: { ChuanEx: 0, ChuanExPer: 0, ChuanExNum: 0 },
      // 判断当前显示的div
      number: 0,
      oldCharts: 0,
      // 涨跌分布y轴数据
      yData1: [], //数据
      // myChartStyle: { width: "100%", height: "100%" }, 图表一借鉴的博客中的残留物
      // 涨跌分布中的数据
      up1: 0,
      down1: 0,
      // 所有股票列表
      tableData: [],
      // 龙虎榜
      hotData: [],
      // 翻页记录，每页数据量，总股票数
      pageNo: 0,
      limit: 50,
      total: 5093,
      // 指数历史趋势图坐标轴数据
      y_green: [],
      y_red: [],
      y_blue: [],
      x: []
    };
  },
   created(){
    this.$store.watch((state)=>{
      return state.loadRise
    },()=>{
      this.loadRise()
    }),
    this.$store.watch((state)=>{
      return state.loadDragon
    },()=>{
      this.loadDragon()
    })
  },
  mounted() {
    // 开盘时间判断
    
    let date = new Date();
    if (
      date.getHours() < 9 ||
      (date.getHours() === 9 && date.getMinutes() <= 30)
    ) {
      this.openTime();
    }
    this.changeExponentColor();
    this.initEcharts1();
    this.getStockData();
    this.change(0);
  },
  methods: {
    // 开盘时间未开始提醒
    openTime() {
      const h = this.$createElement;
      this.$notify({
        title: "温馨提示",
        message: h("i", { style: "color: red" }, "未到开盘时间")
      });
    },
    //获取上证指数、深证指数、创业板指数据并改变颜色
    changeExponentColor() {
      request.get("MarketData/StockIndex/").then(res => {
        this.Shang.ShangEx = res[0].latest_price;
        this.Shang.ShangExPer = res[0].change;
        this.Shang.ShangExNum = res[0].change_amount;
        this.Shen.ShenEx = res[185].latest_price;
        this.Shen.ShenExPer = res[185].change;
        this.Shen.ShenExNum = res[185].change_amount;
        this.Chuan.ChuanEx = res[190].latest_price;
        this.Chuan.ChuanExPer = res[190].change;
        this.Chuan.ChuanExNum = res[190].change_amount;
        if (Math.sign(this.Shang.ShangExPer) == -1) {
          var x = document.querySelectorAll("#ShangExponent");
          for (var i = 0; i < 3; i++) x[i].style.color = "green";
        }
        if (Math.sign(this.Shen.ShenExPer) == -1) {
          var y = document.querySelectorAll("#ShenExponent");
          for (var j = 0; j < 3; j++) y[j].style.color = "green";
        }
        if (Math.sign(this.Chuan.ChuanExPer) == -1) {
          var z = document.querySelectorAll("#ChuanExponent");
          for (var k = 0; k < 3; k++) z[k].style.color = "green";
        }
      });
    },
    // 获取主页股票列表
    getStockData() {
      this.loadingStockTable = true;
      request
        .get("/stock/allStocks/", { params: { pagenum: this.pageNo } })
        .then(res => {
          this.tableData = res;
          this.loadingStockTable = false;
        });
    },
    //获取股票龙虎榜
    getHotData() {
      request.get("MarketData/MostPopular/").then(res => {
        let listObject = res;
        let list = [];
        let title = [];
        for (let var1 in listObject) {
          title.push(var1);
        }
        title.forEach((e, i) => {
          let index = 0;
          for (let var2 in listObject[e]) {
            if (i == 0) {
              list.push({});
            }
            this.$set(list[index], e, listObject[e][var2]);
            index++;
          }
        });
        this.hotData = list;
        this.oldCharts = this.number;
        this.loadingMarketTop = false;
        this.initEcharts1();
      });
    },
    // 上证指数、深证指数、创业板指的历史趋势图
    getIndex() {
      this.$store.commit("setLoadDragon",1);
      request.get("MarketData/HistoryStockIndex/").then(res => {
        this.y_green = res[1];
        this.y_red = res[2];
        this.y_blue = res[3];
        this.x = res[0];
        this.initEcharts3();
        this.$store.commit("setLoadDragon",0);
      });
    },
    // 控制所有股票表格翻页
    handleCurrentChange(page) {
      this.pageNo = page;
      this.getStockData(page - 1);
    },
    // 获取涨跌分布的图表
    getMyChartData() {
      this.$store.commit("setLoadRise",1);
      request.get("/MarketData/UDdistribution/").then(res => {
        this.yData1 = res;
        var temp = 0;
        for (let i = 0; i <= 4; i++) temp = temp + res[i];
        this.up1 = temp;
        var temp1 = 0;
        for (let i = 5; i <= 9; i++) temp1 = temp1 + res[i];
        this.down1 = temp1;
        this.initEcharts1();
        this.$store.commit("setLoadRise",0);
      });
      // 7秒请求一次
      // window.setInterval(() => {
      //   request.get("/UDdistribution/").then(res=>{
      //   console.log(res);
      //   this.yData1=res;
      //   var temp=0;
      //   for(let i=0;i<=4;i++)
      //   temp=temp+res[i];
      //   this.up1=temp;
      //   var temp1=0;
      //   for(let i=5;i<=9;i++)
      //   temp1=temp1+res[i];
      //   this.down1=temp1;
      //   this.initEcharts1();
      // })
      //  }, 1000*7)
    },
    // 判断大盘数据显示哪个表格
    change(index) {
      this.number = index;
      if (this.number === 0) {
        this.getMyChartData();
        this.oldCharts = this.number;
      }
      if (this.number === 1) {
        this.getHotData();
        this.loadingMarketTop = true;
        this.oldCharts = this.number;
      }
      if (this.number === 2) {
        this.getIndex();
        this.oldCharts = this.number;
      }
    },
    // 涨跌分布图表绘制函数
    initEcharts1() {
      // 基本柱状图
      var option = {
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "shadow"
          }
        },
        grid: {
          left: "3%",
          right: "4%",
          bottom: "3%",
          containLabel: true
        },
        xAxis: {
          // nameLocation: 'middle',
          type: "category",
          data: [
            "跌停~-8%",
            "-8%~-6%",
            "-6%~-4%",
            "-4%~-2%",
            "-2%~0",
            "0~2%",
            "2%~4%",
            "4%~6%",
            "6%~8%",
            "8%~涨停"
          ],
          boundaryGap: true,
          axisTick: {
            alignWithLabel: true
          }
        },
        yAxis: {
          type: "value",
          scale: true,
          max: 2500,
          min: 0
          //  boundaryGap: [0.2, 0.2]
        },
        series: [
          {
            type: "bar", //形状为柱状图
            data: this.yData1,
            barWidth: 30,
            itemStyle: {
              normal: {
                color: function(params) {
                  var colorList = [
                    "rgb(89, 184, 129)",
                    "rgb(89, 184, 129)",
                    "rgb(89, 184, 129)",
                    "rgb(89, 184, 129)",
                    "rgb(89, 184, 129)",
                    "rgb(215, 84, 66)",
                    "rgb(215, 84, 66)",
                    "rgb(215, 84, 66)",
                    "rgb(215, 84, 66)",
                    "rgb(215, 84, 66)"
                  ];
                  return colorList[params.dataIndex];
                }
              }
            }
          }
        ]
      };
      // 初始化容器用于实现echarts实例，否则图表不能正常显示
      var lasttemp = "mychart" + this.oldCharts;
      // var nowtemp = "mychart" + this.number;
      var nowtemp = "mychart" + 0;
      var fasterheight = document.getElementById(nowtemp);
      var sonheight = document.getElementById(lasttemp);
      fasterheight.style.height = sonheight.offsetHeight + "px";
      var fasterwidth = document.getElementById(nowtemp);
      var sonwidth = document.getElementById(lasttemp);
      fasterwidth.style.width = sonwidth.offsetWidth + "px";
      var mychart0 = echarts.init(document.getElementById("mychart0"));
      mychart0.showLoading();
      mychart0.setOption(option);
      mychart0.hideLoading();
      //随着屏幕大小调节图表
      window.addEventListener("resize", () => {
        mychart0.resize();
      });
    },
    // 上证指数、深证指数、创业板指图表绘制函数
    initEcharts3() {
      var option = {
        title: {
          text: '三板指数 历史数据',
          x: 'left',
          textStyle: {
            fontSize: 15,
            fontStyle: 'normal', // 主标题文字字体的风格。 'normal'  'italic'  'oblique'
            fontWeight: 'bold', // 主标题文字字体的粗细。 'normal' 'bold'  'bolder'  'lighter' 500|600
          },
        },
        tooltip: {
          trigger: "axis"
        },
        grid: {
          left: "1%",
          right: "4%",
          bottom: "10%",
          containLabel: true
        },
        legend: {
          padding: 10,
          tooltip: {
            show: true
          },
          y: "bottom",
          data: ["上证指数", "深证指数", "创业板指"],
        },
        xAxis: { type: "category", data: this.x },
        yAxis: { type: "value" },
        series: [
          {
            name: "上证指数",
            data: this.y_green,
            type: "line",
            showSymbol: false,
            color: "green"
          },
          {
            name: "深证指数",
            data: this.y_red,
            type: "line",
            showSymbol: false,
            color: "red"
          },
          {
            name: "创业板指",
            data: this.y_blue,
            type: "line",
            showSymbol: false,
            color: "blue"
          }
        ]
      };
      var lasttemp = "mychart" + this.oldCharts;
      // var nowtemp = "mychart" + this.number;
      var nowtemp = "mychart" + 2;
      var fasterheight = document.getElementById(nowtemp);
      var sonheight = document.getElementById(lasttemp);
      fasterheight.style.height = sonheight.offsetHeight + "px";
      var fasterwidth = document.getElementById(nowtemp);
      var sonwidth = document.getElementById(lasttemp);
      fasterwidth.style.width = sonwidth.offsetWidth + "px";
      var mychart2 = echarts.init(document.getElementById("mychart2"));
      mychart2.setOption(option);
      window.addEventListener("resize", () => {
        mychart2.resize();
      });
    },
    // 股票列表跳转股票详情
    toStock(code, name) {
      this.$store.commit("setcode", code);
      this.$store.commit("setcompanyIndex", code);
      this.$store.commit("setcompanyName", name);
      this.$router.push("/stockdisplay");
    },
    // 股票列表跳转股票公司详情
    toCompany(code1, code2) {
      this.$store.commit("setcompanyIndex", code1);
      this.$store.commit("setcompanyName", code2);
      this.$router.push("/companyinfo");
    },
    //股票列表添加收藏
    addCollect(name1, code1) {
      request
        .get("collection/", {
          params: {
            name: name1,
            username: this.$store.state.username,
            code: code1
          }
        })
        .then(res => {
          if (this.$store.state.islogin == 1) {
            if (res.code === "111") {
              this.$notify({
                title: "成功",
                message:
                  "您成功将" + name1 + "(" + code1 + ")" + "加入我的收藏",
                type: "success"
              });
            } else if (res.code === "222") {
              this.$notify.info({
                title: "温馨提示",
                message:
                  "您已将该股票(" + name1 + "(" + code1 + "))" + "加入我的收藏",
                type: "warning"
              });
            }
          } else {
            this.$message({
              showClose: true,
              message: "您未登录，请先登录",
              type: "warning"
            });
            this.$router.push("/Login");
          }
        });
    },
    // headClass rowClass用于设置el-table样式(标题及内容文字居中)
    headClass() {
      //表头居中显示
      return "text-align:center";
    },
    rowClass() {
      //表格数据居中显示
      return "text-align:center";
    },
    loadRise(){
      if (this.$store.state.loadRise==0) {
          // 以服务的方式调用的 Loading 需要异步关闭
          console.log('!')
          this.loading1.close();
      } else if (this.$store.state.loadRise==1) {
        console.log('?')
        this.loading1=Loading.service({ fullscreen: true, text: "拼命加载中",target:document.querySelector('#mychart0')});
      }
    },
    loadDragon(){
          console.log("xixixi");
      if (this.$store.state.loadDragon==0) {
          // 以服务的方式调用的 Loading 需要异步关闭
          this.loading2.close();
          console.log('loading close');
      } else if (this.$store.state.loadDragon==1) {
        this.loading2=Loading.service({ fullscreen: true, text: "拼命加载中",target:document.querySelector('#mychart2')});console.log('loaing start!')
      }
    }
  }
};
</script>

<style scoped>
.MainWindow {
  display: flex;
  flex-direction: column;
  background: #e7e9eb;
  margin: 56px 0px 0px 0px;
}
.head {
  margin: 15px 0;
}
.echartstable {
  display: flex;
  flex-direction: row;
  background: #e7e9eb;
  margin: 0px 60px 0px 60px;
  border-radius: 15px;
  box-shadow: 5px 15px 20px rgba(102, 102, 102, 0.5);
}
.manyCharts {
  flex: 3;
  display: flex;
  background: #e7e9eb;
  border: 4px solid #e7e9eb;
  border-radius: 15px;
}
.echart {
  margin: 0px 0px 0px 2px;
  background: #fdfdfd;
  display: flex;
  border-radius: 15px;
}
.exponent {
  display: flex;
  flex-direction: row;
  justify-content: center;
  height: 200px;
  margin: 20px 45px 0px 63px;
}
.myExponent {
  display: flex;
  margin: 0px 20px 0px 0px;
  background: #fdfdfd;
  flex: 1;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  padding: 2px;
  border-radius: 15px;
  box-shadow: 5px 15px 15px rgba(102, 102, 102, 0.5);
}
.left {
  display: flex;
  flex-direction: column;
  flex: 1;
}
.head h2 {
  display: flex;
  height: 21px;
  color: #000000;
  line-height: 21px;
  font-weight: 700;
  border-left: 6px solid #528fcc;
  padding-left: 10px;
  font-size: 18px;
  overflow: hidden;
  text-shadow: 0px 1px 2px #ffffff, -2px -3px 1px rgb(204, 200, 200);
}
.detail {
  display: flex;
  justify-content: center;
}
.UpDown span {
  margin: 10px;
  display: flex;
}
.image {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  margin: 25px 0px 0px 0px;
}
.beauty {
  flex-direction: column;
  margin: 0 0 0 10%;
}
.titleEx {
  text-shadow: 0px 1px 2px #7a7a7a, -2px -3px 1px rgb(255, 255, 255);
}
#ShangExponent {
  font-size: 16px;
  font-weight: 700;
  color: red;
}
#ShenExponent {
  font-size: 16px;
  font-weight: 700;
  color: red;
}
#ChuanExponent {
  font-size: 16px;
  font-weight: 700;
  color: red;
}
.UpDown {
  flex: 1;
  background: #f5f5f5;
  border: 4px solid #ebebeb;
  border-radius: 15px;
}
.newStyle {
  background: #fff;
  border-left: 6px solid #ff481a;
}
</style>
