<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <div class="card">
    <div class="card-header">{{ title }}</div>
    <div class="card-body">
      <el-table
        :data="tableData"
        style="width: 80%;"
        max-height=430
        :default-sort="{ prop: 'date', order: 'descending' }"
      >
        <el-table-column prop="date" label="日期" sortable width="150">
        </el-table-column>
        <el-table-column prop="code" label="股票代码"> </el-table-column>
        <el-table-column prop="size" label="持仓数量"> </el-table-column>
        <el-table-column prop="price" label="成本价"> </el-table-column>
        <el-table-column prop="present" label="现价"> </el-table-column>
        <el-table-column prop="profit" label="盈亏"> </el-table-column>
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
bus.$on("hold_result", (val) => {
      this.tableData = [];
      //   console.log(val);
      //   console.log(val[0]);
      for (var i = 0; i < val.length; i++) {
        this.tableData[i] = {
          date: val[i][0],
          code: val[i][1],
          size: val[i][2],
          price: val[i][3],
          present: val[i][4],
          profit: val[i][5],
        };
      }
    });
    // this.tableData = JSON.parse(this.$store.state.res["hold_result"]);
    var temphold=JSON.parse(this.$store.state.res)
    var temp= JSON.parse(temphold["hold_result"]);
    console.log(temp)
    this.tableData = [];
    for (var i = 0; i < temp.length; i++) {
      this.tableData[i] = {
        date: temp[i][0],
        code: temp[i][1],
        size: temp[i][2],
        price: temp[i][3],
        present: temp[i][4],
        profit: temp[i][5],
      };
    }
  },
  mounted() {
    bus.$on("hold_result", (val) => {
      this.tableData = [];
      //   console.log(val);
      //   console.log(val[0]);
      for (var i = 0; i < val.length; i++) {
        this.tableData[i] = {
          date: val[i][0],
          code: val[i][1],
          size: val[i][2],
          price: val[i][3],
          present: val[i][4],
          profit: val[i][5],
        };
      }
    });
    // this.tableData = JSON.parse(this.$store.state.res["hold_result"]);
    var temphold=JSON.parse(this.$store.state.res)
    var temp= JSON.parse(temphold["hold_result"]);
    this.tableData = [];
    for (var i = 0; i < temp.length; i++) {
      this.tableData[i] = {
        date: temp[i][0],
        code: temp[i][1],
        size: temp[i][2],
        price: temp[i][3],
        present: temp[i][4],
        profit: temp[i][5],
      };
    }
    console.log(this.tableData);
  },
  methods: {},
  props: ["title"],
};
</script>