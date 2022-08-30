<template>
  <div>
    <b-navbar fill toggleable="lg" type="dark" variant="dark" fixed="top">
      <b-navbar-brand href="#" style="margin-left:11px" @click="click6">SeuQuant</b-navbar-brand>
      <b-navbar-nav class="me-auto">
        <b-nav-item href="#" @click="click1">行情中心</b-nav-item>
        <b-nav-item href="#" @click="click7" v-if="this.$store.state.islogin==1?this.loginshow==false:this.loginshow==true">登录</b-nav-item>
        <b-nav-form>
          <el-autocomplete

              v-model="code"

              :fetch-suggestions="querySearch"
              placeholder="请输入股票代码"
              :trigger-on-focus="false"


          ></el-autocomplete>
        </b-nav-form>
        <b-nav-form>
          <b-button variant="light" class="my-2 my-sm-0" @click="searchstock" style="margin-left: 10px">Search</b-button>

        </b-nav-form>
        <b-nav-item href="#" @click="click3">策略列表</b-nav-item>
        <b-nav-item href="#" @click="click4">回测历史</b-nav-item>
        <b-nav-item type="dark" variant="dark" @click="click5">
          个人中心
        </b-nav-item>
        <b-dropdown :text="this.$store.state.username" type="dark" variant="dark" v-if="this.$store.state.navshow"  offset="50" id="dropdown-right" left style="position: absolute; right: 50px" >
           <b-dropdown-item-button  href="#" @click="setvip">开通VIP</b-dropdown-item-button>
          <b-dropdown-item-button href="#" @click="exitSystem">退出登录</b-dropdown-item-button>
        </b-dropdown>
        

    
        <!-- <b-nav-text style="position: absolute; right: 20px"></b-nav-text> -->
      </b-navbar-nav>

    </b-navbar>

  </div>
</template>

<script>
import request from "@/util/request"
export default {
  name: "TopNavigator",
  data() {
    return {
      code: "",
      navshow:false,
      loginshow:true,
      code_lists:[]
    };
  },
  mounted() {
    this.loadall();
  },
  methods: {
    // Convenience method to scroll a heading into view.
    // Not required for scrollspy to work

    querySearch(queryString, cb) {
      var code_lists = this.code_lists;
      var results = queryString ? code_lists.filter(this.createFilter(queryString)) : code_lists;
      // 调用 callback 返回建议列表的数据
      cb(results);
    },
    createFilter(queryString) {
      return (code_list) => {
        return (code_list.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0);
      };
    },
    loadall(){
      request.get('stock/allStocksCodes/').then(res=>{
        console.log("...")
        this.code_lists=res
      })},

      click6() {
      this.$router.push("/mainwindow");
    },
    click1() {
      this.$router.push("/mainwindow");
    },
    click3() {
      if (this.$store.state.islogin == 1) {
        this.$router.push("/StrategyList");
        this.$store.commit("setFlagLset", 1);
      } else {
        this.$message({
          showClose: true,
          message: "您未登录，请先登录",
          type: "warning"
        });
        this.$router.push("/Login");
      }
    },
    click4() {
      if (this.$store.state.islogin == 1) {
        this.$router.push("/backtesthistory");
        this.$store.commit("setFlagLast", 0);
      } else {
        this.$message({
          showClose: true,
          message: "您未登录，请先登录",
          type: "warning"
        });
        this.$router.push("/Login");
      }
    },
    click7() {
      if (this.$store.state.islogin == 1) {
        this.$message({
          showClose: true,
          message: "您已登录！",
          type: "warning"
        });
        this.$router.push("/mainwindow");
      } else {
        this.$router.push("/Login");
      }
    },
    searchstock() {
      this.$store.commit("setcode", this.code);
      this.$router.push("/stockdisplay");
    },
    click5() {
      if (this.$store.state.islogin == 1) {
        this.$router.push("/userinterface");
      }else{
         this.$message({
          showClose: true,
          message: "您未登录，请先登录",
          type: "warning"
        });
      }
    },
    exitSystem() {
      // if (this.$store.state.islogin == 1) {
         this.$message({
          showClose: true,
          message: "成功退出登录！",
          type: "warning"
        });
        this.$store.commit('setusername',' ');
        console.log("lalallalalala");
        
        console.log(this.$store.state.username);
        this.$store.commit('setuserType',0)
        this.$store.commit("setlogin", 0);
        this.$store.commit('setnavshow',false)
        this.$router.push("/login");
      // }
    },
    setvip(){
      if(this.$store.state.islogin==1){
      
        request.post("/toVip/",{username:this.$store.state.username}).then(
        res=>{ if(res.code=='111'){
           this.$store.commit('setuserType',1)
           this.$message({
              showClose: true,
              message: "开通成功",
              type: "success"
            });
          }
          else{
            this.$message({
              showClose: true,
              message: "开通失败",
              type: "danger"
            });
          }
          }
        )
      }else{
       this.$message({
              showClose: true,
              message: "请先登录",
              type: "warning"
            });
      }
    }
  }
};
</script>


<style>
.el-dropdown-link {
  cursor: pointer;
  color: white;
}
.el-icon-arrow-down {
  font-size: 12px;
}

</style>
