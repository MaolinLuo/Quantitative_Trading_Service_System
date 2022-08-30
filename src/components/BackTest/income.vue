<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <div class="card">
    <div class="card-header">{{ title }}</div>
    <div class="card-body">
      <b-container class="bv-example-row">
        <b-row>
          <b-col>
            <span>剩余持仓价值</span>
            <p
              :class="[indicator_list[0] >= 0 ? 'red' : 'green']"
            >{{ Math.round((indicator_list[0] + Number.EPSILON) * 100) / 100 }}</p>
          </b-col>
          <b-col>
            <span>策略收益</span>

            <p :class="[indicator_list[1] >= 0 ? 'red' : 'green']">
              {{
              (Math.round((indicator_list[1] + Number.EPSILON) * 100) / 100) *
              100 +
              "%"
              }}
            </p>
          </b-col>
          <b-col>
            <span>复合收益总额</span>
            <p :class="[indicator_list[2] >= 0 ? 'red' : 'green']">
              {{
              (Math.round((indicator_list[2] + Number.EPSILON) * 10000) /
              10000) *
              100 +
              "%"
              }}
            </p>
          </b-col>
          <b-col>
            <span>年化收益率</span>
            <p :class="[indicator_list[3] >= 0 ? 'red' : 'green']">
              {{
              Math.round((indicator_list[3] + Number.EPSILON) * 100) / 100 +
              "%"
              }}
            </p>
          </b-col>
          <b-col>
            <span>最大回撤率</span>
            <p :class="[indicator_list[4] >= 0 ? 'red' : 'green']">
              {{
              Math.round((indicator_list[4] + Number.EPSILON) * 100) / 100 +
              "%"
              }}
            </p>
          </b-col>
          <b-col>
            <span>最大回撤金额</span>
            <p
              :class="[indicator_list[5] >= 0 ? 'red' : 'green']"
            >{{ Math.round((indicator_list[5] + Number.EPSILON) * 100) / 100 }}</p>
          </b-col>
          <b-col>
            <span>年化夏普比率</span>
            <p :class="[indicator_list[6] >= 0 ? 'red' : 'green']">
              {{
              Math.round((indicator_list[6] + Number.EPSILON) * 100) / 100 +
              "%"
              }}
            </p>
          </b-col>
        </b-row>
      </b-container>
      <b-container>
        <!-- 调整宽高 -->
        <div ref="main" style="height:380px;width:80%"></div>
      </b-container>
    </div>
  </div>
</template>
<script>
import * as echarts from "echarts";
import request from "@/util/request";
import bus from "../eventBus";

export default {
  data() {
    return {
      indicator_list: [],
      hold_result: [],
      trade_result: [],
      value_ratio: [],
      benchmark: []
    };
  },
  mounted() {
    this.getData();
  },
  created(){
    console.log("create")
this.getData()
  },
  methods: {
    getData() {
      let chartDom = this.$refs.main;
      let myChart = echarts.init(chartDom);
      myChart.showLoading();
      if (this.name == "海龟交易策略") {
        this.$store.commit('setIncomeFlag',true)
        request
          .post("/strategy/turtle/", {
            strategy:this.name,
            backtest_id: this.backtest_id,
            username: this.$store.state.username,
            stocks: this.codes.toString(),
            startDate: this.startDate.replace(/-/g, ""),
            endDate: this.endDate.replace(/-/g, "")
          })
          .then(res => {
            if (res.code == "333") {
              this.$message.error("有不存在的股票，请输入正确的股票代码！");
              setTimeout(this.$router.push("/StrategyList"), 3000);
            } else if (res.code == "222") {
              this.$message.error(
                "查询到相同的回测记录名，请输入不同的回测名称！"
              );
              setTimeout(this.$router.push("/StrategyList"), 3000);
            } else {
              this.hold_result = [];
              this.trade_result = [];
              this.value_ratio = [];
              this.benchmark = [];
              this.indicator_list = res["indicator_list"];
              this.hold_result = JSON.parse(res["hold_result"]);
              this.trade_result = JSON.parse(res["trade_result"]);
              this.value_ratio = JSON.parse(res["value_ratio"]);
              this.benchmark = JSON.parse(res["benchmark"]);
              bus.$emit("trade_result", this.trade_result);
              bus.$emit("hold_result", this.hold_result);
              this.initChart(myChart);
            }
          })
          .catch(e => {
            console.log(e);
          });
      } else if (this.name == "双均线策略") {
        this.$store.commit('setIncomeFlag',true)
        request
          .post("/strategy/sma/", {
            strategy:this.name,
            backtest_id: this.backtest_id,
            username: this.$store.state.username,
            stocks: this.codes.toString(),
            startDate: this.startDate.replace(/-/g, ""),
            endDate: this.endDate.replace(/-/g, "")
          })
          .then(res => {
            if (res.code == "333") {
              this.$message.error("有不存在的股票，请输入正确的股票代码！");
              setTimeout(this.$router.push("/StrategyList"), 3000);
            } else if (res.code == "222") {
              this.$message.error(
                "查询到相同的回测记录名，请输入不同的回测名称！"
              );
              setTimeout(this.$router.push("/StrategyList"), 3000);
            } else {
              this.hold_result = [];
              this.trade_result = [];
              this.value_ratio = [];
              this.benchmark = [];
              this.indicator_list = res["indicator_list"];
              this.hold_result = JSON.parse(res["hold_result"]);
              this.trade_result = JSON.parse(res["trade_result"]);
              this.value_ratio = JSON.parse(res["value_ratio"]);
              this.benchmark = JSON.parse(res["benchmark"]);
              bus.$emit("trade_result", this.trade_result);
              bus.$emit("hold_result", this.hold_result);
              this.initChart(myChart);
            }
          })
          .catch(e => {
            console.log(e);
          });
      } else if (this.name == "凯特勒策略") {
        this.$store.commit('setIncomeFlag',true)
        request
          .post("/strategy/keltner/", {
            strategy:this.name,
            backtest_id: this.backtest_id,
            username: this.$store.state.username,
            stocks: this.codes.toString(),
            startDate: this.startDate.replace(/-/g, ""),
            endDate: this.endDate.replace(/-/g, "")
          })
          .then(res => {
            if (res.code == "333") {
              this.$message.error("有不存在的股票，请输入正确的股票代码！");
              setTimeout(this.$router.push("/StrategyList"), 3000);
            } else if (res.code == "222") {
              this.$message.error(
                "查询到相同的回测记录名，请输入不同的回测名称！"
              );
              setTimeout(this.$router.push("/StrategyList"), 3000);
            } else {
              this.hold_result = [];
              this.trade_result = [];
              this.value_ratio = [];
              this.benchmark = [];
              this.indicator_list = res["indicator_list"];
              this.hold_result = JSON.parse(res["hold_result"]);
              this.trade_result = JSON.parse(res["trade_result"]);
              this.value_ratio = JSON.parse(res["value_ratio"]);
              this.benchmark = JSON.parse(res["benchmark"]);
              bus.$emit("trade_result", this.trade_result);
              bus.$emit("hold_result", this.hold_result);
              this.initChart(myChart);
            }
          })
          .catch(e => {
            console.log(e);
          });
      } else if (this.name == "布林带策略") {
        this.$store.commit('setIncomeFlag',true)
        request
          .post("/strategy/boll/", {
            strategy:this.name,
            backtest_id: this.backtest_id,
            username: this.$store.state.username,
            stocks: this.codes.toString(),
            startDate: this.startDate.replace(/-/g, ""),
            endDate: this.endDate.replace(/-/g, "")
          })
          .then(res => {
            if (res.code == "333") {
              this.$message.error("有不存在的股票，请输入正确的股票代码！");
              setTimeout(this.$router.push("/StrategyList"), 3000);
            } else if (res.code == "222") {
              this.$message.error(
                "查询到相同的回测记录名，请输入不同的回测名称！"
              );
              setTimeout(this.$router.push("/StrategyList"), 3000);
            } else {
              this.hold_result = [];
              this.trade_result = [];
              this.value_ratio = [];
              this.benchmark = [];
              this.indicator_list = res["indicator_list"];
              this.hold_result = JSON.parse(res["hold_result"]);
              this.trade_result = JSON.parse(res["trade_result"]);
              this.value_ratio = JSON.parse(res["value_ratio"]);
              this.benchmark = JSON.parse(res["benchmark"]);
              bus.$emit("trade_result", this.trade_result);
              bus.$emit("hold_result", this.hold_result);
              this.initChart(myChart);
            }
          })
          .catch(e => {
            console.log(e);
          });
      } else if (this.name == "基于GRU预测策略") {
        
        
        this.$store.commit('setIncomeFlag',true)
        request
          .post("/strategy/gru/", {
            strategy:this.name,
            backtest_id: this.backtest_id,
            username: this.$store.state.username,
            stocks: this.code_ai,
            startDate: this.startDate.replace(/-/g, ""),
            endDate: this.endDate.replace(/-/g, ""),
            epoch: this.epoch,
            steps: this.steps,
            rate: this.rate,
            stock_size: this.stock_size
          })
          .then(res => {
            if (res.code == "333") {
              this.$message.error("有不存在的股票，请输入正确的股票代码！");
              setTimeout(this.$router.push("/StrategyList"), 3000);
            } else if (res.code == "222") {
              this.$message.error(
                "查询到相同的回测记录名，请输入不同的回测名称！"
              );
              setTimeout(this.$router.push("/StrategyList"), 3000);
            } else {
              this.hold_result = [];
              this.trade_result = [];
              this.value_ratio = [];
              this.benchmark = [];
              this.indicator_list = res["indicator_list"];
              this.hold_result = JSON.parse(res["hold_result"]);
              this.trade_result = JSON.parse(res["trade_result"]);
              this.value_ratio = JSON.parse(res["value_ratio"]);
              this.benchmark = JSON.parse(res["benchmark"]);
              bus.$emit("trade_result", this.trade_result);
              bus.$emit("hold_result", this.hold_result);
              this.initChart(myChart);
            }
          })
          .catch(e => {
            console.log(e);
          });
      } else if (this.name == "基于RNN预测策略") {
     
      
         
         this.$store.commit('setIncomeFlag',true)
         request
          .post("/strategy/rnn/", {
            strategy:this.name,
            backtest_id: this.backtest_id,
            username: this.$store.state.username,
            stocks: this.code_ai,
            startDate: this.startDate.replace(/-/g, ""),
            endDate: this.endDate.replace(/-/g, ""),
            epoch: this.epoch,
            steps: this.steps,
            rate: this.rate,
            stock_size: this.stock_size
          })
          .then(res => {
            if (res.code == "333") {
              this.$message.error("有不存在的股票，请输入正确的股票代码！");
              setTimeout(this.$router.push("/StrategyList"), 3000);
            } else if (res.code == "222") {
              this.$message.error(
                "查询到相同的回测记录名，请输入不同的回测名称！"
              );
              setTimeout(this.$router.push("/StrategyList"), 3000);
            } else {
              console.log("rnn")
              this.hold_result = [];
              this.trade_result = [];
              this.value_ratio = [];
              this.benchmark = [];
              this.indicator_list = res["indicator_list"];
              this.hold_result = JSON.parse(res["hold_result"]);
              this.trade_result = JSON.parse(res["trade_result"]);
              this.value_ratio = JSON.parse(res["value_ratio"]);
              this.benchmark = JSON.parse(res["benchmark"]);
              bus.$emit("trade_result", this.trade_result);
              bus.$emit("hold_result", this.hold_result);
              this.initChart(myChart);
            }
          })
          .catch(e => {
            console.log(e);
          });
      } else if (this.name == "基于LSTM预测策略") {
      
     
        this.$store.commit('setIncomeFlag',true)
        request
          .post("/strategy/lstm/", {
            strategy:this.name,
            backtest_id: this.backtest_id,
            username: this.$store.state.username,
            stocks: this.code_ai,
            startDate: this.startDate.replace(/-/g, ""),
            endDate: this.endDate.replace(/-/g, ""),
            epoch: this.epoch,
            steps: this.steps,
            rate: this.rate,
            stock_size: this.stock_size
          })
          .then(res => {
            if (res.code == "333") {
              this.$message.error("有不存在的股票，请输入正确的股票代码！");
              setTimeout(this.$router.push("/StrategyList"), 3000);
            } else if (res.code == "222") {
              this.$message.error(
                "查询到相同的回测记录名，请输入不同的回测名称！"
              );
              setTimeout(this.$router.push("/StrategyList"), 3000);
            } else {
              this.hold_result = [];
              this.trade_result = [];
              this.value_ratio = [];
              this.benchmark = [];
              this.indicator_list = res["indicator_list"];
              this.hold_result = JSON.parse(res["hold_result"]);
              this.trade_result = JSON.parse(res["trade_result"]);
              this.value_ratio = JSON.parse(res["value_ratio"]);
              this.benchmark = JSON.parse(res["benchmark"]);
              bus.$emit("trade_result", this.trade_result);
              bus.$emit("hold_result", this.hold_result);
              this.initChart(myChart);
            }
          })
          .catch(e => {
            console.log(e);
          });
      } else if (this.name == "MFI策略") {
        this.$store.commit('setIncomeFlag',true)
        request
          .post("/strategy/mfi/", {
            strategy:this.name,
            backtest_id: this.backtest_id,
            username: this.$store.state.username,
            stocks: this.codes.toString(),
            startDate: this.startDate.replace(/-/g, ""),
            endDate: this.endDate.replace(/-/g, ""),
          })
          .then(res => {
            if (res.code == "333") {
              this.$message.error("有不存在的股票，请输入正确的股票代码！");
              setTimeout(this.$router.push("/StrategyList"), 3000);
            } else if (res.code == "222") {
              this.$message.error(
                "查询到相同的回测记录名，请输入不同的回测名称！"
              );
              setTimeout(this.$router.push("/StrategyList"), 3000);
            } else {
              this.hold_result = [];
              this.trade_result = [];
              this.value_ratio = [];
              this.benchmark = [];
              this.indicator_list = res["indicator_list"];
              this.hold_result = JSON.parse(res["hold_result"]);
              this.trade_result = JSON.parse(res["trade_result"]);
              this.value_ratio = JSON.parse(res["value_ratio"]);
              this.benchmark = JSON.parse(res["benchmark"]);
              bus.$emit("trade_result", this.trade_result);
              bus.$emit("hold_result", this.hold_result);
              this.initChart(myChart);
            }
          })
          .catch(e => {
            console.log(e);
          });
      } else {
        this.$store.commit('setIncomeFlag',true)
        this.hold_result = [];
        this.trade_result = [];
        this.value_ratio = [];
        this.benchmark = [];
        // sherry change
        // console.log(this.indicator_list);
        // console.log(this.hold_result);
        var tempres=JSON.parse(this.$store.state.res)
        this.indicator_list = tempres["indicator_list"];
        console.log(tempres["indicator_list"])
        this.hold_result = JSON.parse(tempres["hold_result"]);
        this.trade_result = JSON.parse(tempres["trade_result"]);
        this.value_ratio = JSON.parse(tempres["value_ratio"]);
        this.benchmark = JSON.parse(tempres["benchmark"]);
        // var temp1 = JSON.parse(this.$store.state.res["value_ratio"]);
        // for (var i in temp1) {
        //   var item = [];
        //   for (var j in temp1[i]) {
        //     item.push(temp1[i][j]);
        //   }
        //   this.value_ratio.push(item);
        // }
        // var temp = JSON.parse(this.$store.state.res["benchmark"]);
        // for (var m in temp) {
        //   var item2 = [];
        //   for (var n in temp[m]) {
        //     item2.push(temp[m][n]);
        //   }
        //   this.benchmark.push(item2);
        // }
        // console.log(this.benchmark);
        this.initChart(myChart);
        window.addEventListener("resize", () => {
          myChart.resize();
        });
      }
    },
    initChart(myChart) {
      var option = {
        tooltip: {
          trigger: "axis",
          valueFormatter: value => value + "%",
          position: function(pt) {
            return [pt[0], "10%"];
          }
        },
        legend: {},
        toolbox: {
          feature: {
            dataZoom: {
              yAxisIndex: "none"
            },
            restore: {},
            saveAsImage: {}
          }
        },
        xAxis: {
          type: "category",
          axisLine: { show: false },
          axisTick: { show: false }
        },
        yAxis: {
          type: "value",
          position: "right",
          axisLine: { show: false },
          axisTick: { show: false },
          axisLabel: {
            formatter: function(value) {
              return value.toString() + "%";
            }
          }
        },
        dataZoom: [
          {
            type: "inside"
          },
          {}
        ],
        series: [
          {
            name: "策略收益",
            type: "line",
            // smooth: true,
            symbol: "none",
            areaStyle: {},
            data: this.value_ratio
          },
          {
            name: "基准收益",
            type: "line",
            // smooth: true,
            symbol: "none",
            color: "brown",
            data: this.benchmark
          }
        ]
      };

      myChart.hideLoading();
      myChart.clear();
      this.$store.commit('setIncomeFlag',false)
      myChart.resize();
      myChart.setOption(option,false);
      window.addEventListener("resize", () => {
        myChart.resize();
      });
    }
  },
  props: [
    "title",
    "name",
    "startDate",
    "endDate",
    "epoch",
    "steps",
    "rate",
    "stock_size",
    "code_ai",
    "codes",
    "backtest_id"
  ]
};
</script>
<style scoped>
.card-body {
  justify-content: center;
  align-items: center;
}
span {
  color: gray;
  font-size: 8px;
}
.red {
  color: red;
}
.green {
  color: green;
}
</style>