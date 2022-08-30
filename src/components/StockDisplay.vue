<template>
  <div class="wrapper">
    <div class="detailpage-wrapper">
      <div class="left-area">
        <div class="top-block">
          <div class="top-block-left">
            <div class="top-block-left prod-name">
              <span class="cn">{{this.title}}</span>
            </div>
            <div class="price-wrapper">
              <div
                :class="[tableData['涨跌']>0?'price-lastpx gt':'price-lastpx dt']"
              >{{tableData['最新价']}}</div>
              <div
                :class="[tableData['涨跌']>0?'price-precision gt':'price-precision dt']"
                style="padding-left: 10px"
              >{{tableData['涨跌']}}</div>
              <div :class="[tableData['涨跌']>0?'price-rate gt':'price-rate dt']">{{newpar}}</div>
            </div>
            <div class="date-status">
              <div class="date">{{time}}</div>
            </div>
          </div>
          <div>
            <el-button type="primary" @click="toCompany()">查看公司资料</el-button>
          </div>
        </div>
        <div class="block">
          <div class="chart-wrapper">
            <router-view ref="kline"></router-view>
          </div>
        </div>
      </div>
      <div class="right-area">
        <div class="right-area stock-zhibiao-title">
          <h2>最新指标</h2>
        </div>
        <div class="stock-zhibiao">
          <div class="zhibiao-item" v-for="(value,key,index) in tableData" :key="index">
            <span class="zhibiao-item-label">{{key}}</span>
            <span
              :class="[tableData['涨跌']>0?'zhibiao-item-text -market-color--rise':'zhibiao-item-text -market-color--down']"
            >{{value}}</span>
          </div>
          <div class="zhibiao-item" v-for="(value,key,index) in baseData" :key="index">
            <span class="zhibiao-item-label">{{key}}</span>
            <span class="zhibiao-item-text">{{value}}</span>
          </div>
        </div>
        <div class="right-area stock-zhibiao-title">
          <h2>热门快讯</h2>
        </div>
        <div class="stock-zhibiao">
          <div class="zhibiao-item" v-for="(item,index) in industrydata" :key="index">
            <a class="zhuti-event-item">{{item}}</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import request from "@/util/request";

export default {
  name: "StockDisplay",
  data() {
    return {
      tableData: {},
      baseData: {},
      newpar: "",
      title: "",
      time: new Date(),
      industrydata: []
    };
  },

  mounted() {
    this.initTableData();
    this.initBaseData();
    this.inittop();
    console.log("father mount");
  },
  created() {
    this.$store.watch(
      state => {
        return state.code;
      },
      () => {
        console.log("father watch");
        this.initTableData();
        this.initBaseData();
        this.inittop();
      }
    );
    console.log("father create");

    this.currentTime();
  },
  methods: {
    getnowtime() {
      this.time = new Date();
    },
    currentTime() {
      setInterval(this.getnowtime, 500);
    },
    initTableData() {
      //  window.setInterval(()=>{
      request
        .get("stock/realTableData/", {
          params: { code: this.$store.state.code }
        })
        .then(res => {
          if (res.code != "222") {
            this.tableData = res[0];
            this.title = this.tableData["名称"];
            delete this.tableData["名称"];
            var temp = "(" + res[0]["涨跌幅"] + ")";
            this.newpar = temp;
          }
          //  },3000)
        });
    },
    initBaseData() {
      // window.setInterval(()=>{
      request
        .get("stock/realBaseData/", {
          params: { code: this.$store.state.code }
        })
        .then(res => {
          if (res.code != "222") {
            this.baseData = res[0];
          }
        });
      // },3000)
    },
    inittop() {
      request.get("/news/top4").then(res => {
        if (res.code != "222") {
          console.log(res);
          this.industrydata = res;
        }
      });
    },
    toCompany(){
      this.$router.push("/companyinfo");
    }
  }
};
</script>

<style scoped>
.layout-default .wrapper {
  min-height: calc(100vh - 623px);
}

.wrapper {
  width: 1260px;
  margin: 0 auto;
}
*,
*::before,
*::after {
  box-sizing: inherit;
}
user agent stylesheet div {
  display: block;
}
.detailpage-wrapper {
  display: flex;
  justify-content: space-between;
}
.left-area {
  width: 944px;
  padding: 30px 30px 0px;
  background: #fff;
}
.block {
  margin-bottom: 20px;

  background: #fff;
}
.top-block {
  display: flex;
  align-items: center;
  padding-top: 40px;
  justify-content: space-between;
  height: 160px;
}
.chart-wrapper {
  position: relative;
  display: inline-block;
  width: 884px;
  padding-top: 10px;
}
.info-wrapper {
  width: 100%;
}
.top-block-left {
  display: flex;
  flex-direction: column;
}
.top-block-left .prod-name {
  color: #222;
  font-size: 30px;
  align: left;
}
.top-block-left .prod-name .cn {
  line-height: 0px;
}
.top-block-left .price-wrapper {
  display: flex;
  align-items: flex-end;
  margin-top: 0px;
  height: 70px;
  padding-left: 0px;
}
.top-block-left .price-wrapper .price-lastpx {
  font-size: 36px;
  line-height: 36px;
  font-weight: bolder;
}
.top-block-left .price-wrapper .price-precision,
.top-block-left .price-wrapper .price-rate {
  font-size: 20px;
  line-height: 26px;
  margin-right: 4px;
}
.gt {
  color: #ff5959;
}
.dt {
  color: #22e577;
}
.top-block-left .date-status {
  margin-top: 6px;
  font-size: 14px;
  display: flex;
  align-items: flex-end;
}
.top-block-left .date-status .status {
  line-height: 16px;
  color: #222;
}
.top-block-left .date-status .date {
  line-height: 14px;
  color: #999;
}
.right-area {
  padding-top: 30px;
  width: 300px;
}
.right-area .stock-zhibiao-title {
  display: block;
  position: relative;
  font-size: 16px;
  color: #333;
  letter-spacing: 0;
  text-align: left;
  height: 24px;
  padding-left: 0px;
}
.stock-zhibiao {
  display: -webkit-box;
  display: flex;
  flex-wrap: wrap;
  padding-top: 10px;
}
.stock-news {
  display: flex;
  flex-wrap: wrap;
  padding-top: 10px;
}
h2 {
  height: 21px;
  line-height: 21px;
  font-weight: 700;
  border-left: 6px solid #b70822;
  padding-left: 10px;
  font-size: 20px;
  overflow: hidden;
}

.stock-zhibiao .zhibiao-item {
  width: 50%;
  padding: 24px 24px 12px 0;
  display: -webkit-box;
  display: flex;
  -webkit-box-pack: justify;
  justify-content: space-between;
}
.stock-zhibiao .zhibiao-item-label {
  display: block;
  font-size: 14px;
  color: #666;
  letter-spacing: 0;
  text-align: left;
  line-height: 14px;
}
.stock-zhibiao .zhibiao-item-text.-market-color--rise {
  color: #e52222;
}
.stock-zhibiao .zhibiao-item-text.-market-color--down {
  color: #22e577;
}
.stock-zhibiao .zhibiao-item-text {
  display: block;
  font-size: 14px;
  color: #333;
  letter-spacing: 0;
  font-weight: 500;
  text-align: right;
  line-height: 14px;
}
.zhuti-event-item {
  display: -webkit-box;
  display: flex;
  position: relative;
  cursor: pointer;
  background: #fafafa;
  color: #b70822;
}
a {
  text-decoration: none;
}
</style>