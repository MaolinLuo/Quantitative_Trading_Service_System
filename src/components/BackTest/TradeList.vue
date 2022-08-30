<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <div class="card">
    <div class="card-header">{{ title }}</div>
    <div class="card-body">
      <el-table
        :data="tableData"
        style="width: 80%"
        max-height="420px"
        :default-sort="{ prop: 'date', order: 'descending' }"
      >
        <el-table-column prop="date" label="日期" sortable width="150">
        </el-table-column>
        <el-table-column prop="code" label="股票代码"> </el-table-column>
        <el-table-column prop="isbuy" label="交易类型"> </el-table-column>
        <el-table-column prop="vol" label="成交数量"> </el-table-column>
        <el-table-column prop="price" label="成交价"> </el-table-column>
        <el-table-column prop="amount" label="成交额"> </el-table-column>
      </el-table>
    </div>
  </div>
</template>
<script>
import bus from "../eventBus";
export default {
  data() {
    return {
      tableData: [],
    };
  },
  created(){
bus.$on("trade_result", (val) => {
      this.tableData = [];
      //   console.log(val);
      //   console.log(val[0]);
      for (var i = 0; i < val.length; i++) {
        this.tableData[i] = {
          date: val[i][0],
          code: val[i][1],
          isbuy: val[i][2] == "sell" ? "卖出" : "买入",
          vol: val[i][3],
          price: val[i][4],
          amount: val[i][5],
        };
      }
    });
    // this.tableData = JSON.parse(this.$store.state.res["trade_result"]);
    // syj
    var temphold=JSON.parse(this.$store.state.res)
    var temp= JSON.parse(temphold["trade_result"]);
    this.tableData = [];
    for (var i = 0; i < temp.length; i++) {
      this.tableData[i] = {
        date: temp[i][0],
        code: temp[i][1],
        isbuy: temp[i][2]== "sell" ? "卖出" : "买入",
        vol: temp[i][3],
        price: temp[i][4],
        amount: temp[i][5],
      };
    }
  },
  mounted() {
    bus.$on("trade_result", (val) => {
      this.tableData = [];
      //   console.log(val);
      //   console.log(val[0]);
      for (var i = 0; i < val.length; i++) {
        this.tableData[i] = {
          date: val[i][0],
          code: val[i][1],
          isbuy: val[i][2] == "sell" ? "卖出" : "买入",
          vol: val[i][3],
          price: val[i][4],
          amount: val[i][5],
        };
      }
    });
    // this.tableData = JSON.parse(this.$store.state.res["trade_result"]);
    // syj
   var temphold=JSON.parse(this.$store.state.res)
    var temp= JSON.parse(temphold["trade_result"]);
    console.log(temp)
    this.tableData = [];
    for (var i = 0; i < temp.length; i++) {
      this.tableData[i] = {
        date: temp[i][0],
        code: temp[i][1],
        isbuy: temp[i][2]== "sell" ? "卖出" : "买入",
        vol: temp[i][3],
        price: temp[i][4],
        amount: temp[i][5],
      };
    }

  },
  methods: {},
  props: ["title"],
};
</script>