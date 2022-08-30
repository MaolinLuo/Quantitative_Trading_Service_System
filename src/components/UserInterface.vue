<template>
  <div class="userInterface">
    <div class="left">
      <img src="../assets/SeuQuantLogo.png" style="width:80%;border:none;margin:20px 10px 0px 10px" />
      <img src="../assets/ai.jpeg" style="width:40%;margin:10%;display:flex;" />
      <tr
        style="color:white;font-weight:bold;font-size:20px;text-shadow: 1px 1px 1px #000000, -1px -1px 1px rgb(73, 73, 73);"
      >{{this.$store.state.username}}</tr>
      
    </div>
    <div class="main">
      <div class="head">
        <h2>我的收藏</h2>
      </div>
      <div class="tableView">
        <el-table
          :data="tableData"
          :header-cell-style="headClass"
          :cell-style="rowClass"
          :max-height=500
          v-loading="loading"
          element-loading-text="拼命加载中"
        >
          <el-table-column prop="code" label="代码">
            <template slot-scope="scope">
              <a
                target="_blank"
                class="buttonText"
                @click="toStock(scope.row.code)"
              >{{scope.row.code}}</a>
            </template>
          </el-table-column>
          <el-table-column prop="name" label="名称">
          </el-table-column>
          <el-table-column prop="present_price" label="最新价" >
            <template scope="scope">
              <span v-if="scope.row.range>=0" style="color:red">{{ scope.row.present_price}}</span>
              <span v-else style="color:green">{{ scope.row.present_price}}</span>
            </template>
          </el-table-column>
          <el-table-column prop="open" label="开盘价">  
          </el-table-column>
          <el-table-column prop="amount" label="成交量">
          </el-table-column>
          <el-table-column prop="high" label="最高"></el-table-column>
          <el-table-column prop="range" label="涨跌幅">
             <template scope="scope">
              <span v-if="scope.row.range>=0" style="color:red">{{ scope.row.range}}</span>
              <span v-else style="color:green">{{ scope.row.range}}</span>
            </template>
          </el-table-column>
          <el-table-column fixed="right" label="操作">
            <template slot-scope="scope">
              <el-button
                size="mini"
                type="danger"
                @click="handleDelete(scope.row.code,scope.row.name)"
              >删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
  </div>
</template>
<script>
import request from "@/util/request";
export default {
  data() {
    return {
      tableData: [],
      loading:true,
    };
  },
  mounted() {
    this.getTableIndex();
  },
  methods: {
    headClass() {
      //表头居中显示
      return "text-align:center";
    },
    rowClass() {
      //表格数据居中显示
      return "text-align:center";
    },
    handleDelete(tempCode, tempName) {
      request
        .get("collection/removeColl/", {
          params: { username: this.$store.state.username, code: tempCode }
        })
        .then(res => {
          if (res.code === "111") {
            this.$notify({
              title: "成功",
              message:
                "您成功将" + tempName + "(" + tempCode + ")从我的收藏中删除",
              type: "success"
            });
            window.history.go(0);
          } else if (res.code === "222") {
            this.$notify({
              title: "温馨提示",
              message:
                "您未将" +
                tempName +
                "(" +
                tempCode +
                ")" +
                "加入收藏，删除失败",
              type: "warning"
            });
          }
        });
    },
    getTableIndex() {
      this.loading=true;
      request
        .get("collection/list/", {
          params: { username: this.$store.state.username }
        })
        .then(res => {
          console.log(res);
          this.tableData = res;
          console.log(this.tableData);
          this.loading=false;
        });
    }
  }
};
</script>
<style scoped>
.userInterface {
  display: flex;
  flex-direction: row;
  background: #e7e9eb;
  height: 600px;
  margin: 56px 0px 0px 0px;
}
.main {
  display: flex;
  width:70%;
  flex-direction: column;
  justify-items: center;
}
.left {
  display: flex;
  flex-direction: column;
  width: 30%;
  align-content: center;
  align-items: center;
  background-color: #a1a1a1;
}
.tableView {
  display: flex;
  flex-direction: column;
  background: #a5a5a5;
  margin: 0px 30px 0px 30px;
  border-radius: 15px;
  box-shadow: 15px 15px 20px 5px rgba(102, 102, 102, 0.5);
}
.head {
  display: flex;
  flex-direction: column;
  height: 50px;
  margin: 0px 0px 20px 0px;
}
.head h2 {
  display: flex;
  height: 30px;
  font-weight: bolder;
  border-left: 10px solid #c70000;
  padding-top: 3px;
  padding-left: 10px;
  font-size: 20px;
  color: rgb(42, 42, 42);
  text-shadow: 1px 1px 1px #ffffff, -1px -1px 1px rgb(73, 73, 73);
  margin: 10px;
}
h1 {
  font-size: 50px;
  margin: 20px 0px 0px 0px;
  color: rgb(0, 0, 0);
  font-family: STXingkai;
  text-shadow: 1px 1px 1px #000000, -1px -2px 6px rgb(73, 73, 73);
  padding: 0px 0px 0px 100px;
}
h3 {
  font-size: 40px;
  margin: 50px 0px 0px 0px;
  color: rgb(0, 0, 0);
  line-height: 0px;
  font-family: STXingkai;
  text-shadow: 1px 2px 5px #fcfafa, -1px -2px 6px rgb(160, 160, 160);
}
/* .tableView>>>.el-table{
  overflow-x: auto;
  overflow-y: auto;
} */
</style>