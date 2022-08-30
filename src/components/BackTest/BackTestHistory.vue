<template>
<div style="height:600px;width:100%;margin:56px 0 0 0">
  <el-table
      :data="tableData.filter(data => !search || data.backtest_id.toLowerCase().includes(search.toLowerCase()))"
      style="width: 100%" >
    <el-table-column
        label="策略名称"
        prop="strategy">
    </el-table-column>
    <el-table-column
        label="回测记录名称"
        prop="backtest_id">
    </el-table-column>
    <el-table-column
        label="回测开始时间"
        prop="start_date">
    </el-table-column>
    <el-table-column
        label="回测结束时间"
        prop="end_date">
    </el-table-column>
    <el-table-column
        label="回测股票组合"
        prop="stocks">
    </el-table-column>
    <!-- <el-table-column
        label="最大回撤"
        prop="maxdrawdown">
    </el-table-column> -->

    <el-table-column
        align="right" >
      <template slot="header" slot-scope="scope">
        <el-input
            v-model="search"
            size="mini"
            placeholder="输入关键字搜索" @click="enter(scope)"></el-input>
      </template>
      <template slot-scope="scope">
        <el-button
            size="mini"
            type="primary"
            round
            @click="Queryhistory(scope.row.strategy,scope.row.start_date,scope.row.end_date,scope.row.backtest_id)">查询</el-button>
               <el-button
          size="mini"
          type="danger"
          round
          @click="deletehistory(scope.row.backtest_id)">删除</el-button>
      </template>
      
    </el-table-column>

  </el-table>

</div>
</template>

<script>

import request from "@/util/request";


export default {
  name: "BackTestHistory",
  data() {
    return {
      tableData: [
        {name:'111',backtestname:'111'},
        {name:'222'}
      ],
      search: ''
    }
  },
  
  mounted() {
    this.initTableData()
  },
  methods:{
    initTableData() {
      
      request.get('strategy/getBacktestRecords/',{params:{username:this.$store.state.username}}).then(res=>{
        console.log(res)
        this.tableData=res
        console.log(res)
      })
    },
    Queryhistory(strategy,start_date,end_date,backtestname){
      console.log(backtestname)
      request.get("strategy/getSingleBacktestRecord/",{params:{username:this.$store.state.username,backtest_id:backtestname}}).then(
          res=>{
            console.log(res)
            this.$store.commit('setRes',JSON.stringify(res))

            this.$router.push({
              path: "/backtestdisplay",
              query: {
                name:strategy+" ",
                startDate: start_date,
                endDate:end_date
              }
            });
          }
      )
    },
    deletehistory(id){
      console.log("...")
      request.get("strategy/deleteSingleBackTestRecord/",{params:{username:this.$store.state.username,backtest_id:id}}).then(res=>{
        if(res.code=='111'){
          this.$message({
              showClose: true,
              message: "成功删除",
              type: "success"
            });
            history.go(0)
        }
      })
    }
    
  },

}
</script>

<style scoped>
element.style {
  min-height: 450px;
}
.content.content-area.old-style {
  overflow: hidden;
}
.padding_b0 {
  padding-bottom: 0!important;
}
* {
  padding: 0;
  margin: 0;
}
* {
  -webkit-box-sizing: border-box;
  -moz-box-sizing: border-box;
  box-sizing: border-box;
}
div {
  display: block;
}
</style>