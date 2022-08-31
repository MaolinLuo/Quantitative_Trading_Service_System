<template>
  <div class="login">
    <TopNavigator></TopNavigator>
    <img :src="imgSrc" width="100%" height="100%" alt />
    <div class="loginPart">
      <h2 style="margin:20px;">SeuQuant用户登录</h2>
      <el-form>
        <div class="inputElement">
          <el-input v-model="username" placeholder="请输入用户名 "></el-input>
        </div>
        <div class="inputElement">
          <el-input v-model="password" placeholder="请输入密码 " type="password" @keyup.enter.native="login()"></el-input>
        </div>
        <div class="rowDisplay" style="margin:10px 0px 0px 10px;">
        <div style="padding-right:40px;">
          <el-button type="primary" @click="login()" >登录</el-button>
        </div>
        <div style="text-align: right;color: white;">
          <el-link type="warning" @click="routeregister">没有账号？去注册</el-link>
        </div>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script>
import request from "@/util/request";
import TopNavigator from "@/components/TopNavigator";

export default {
  name: "LoginView",
  components: {
    TopNavigator
  },
 mounted(){
   this.$store.commit("setnavshow",false)
 },
  data() {
    return {
      imgSrc: require("../assets/dollar.webp"),
      username: "",
      password: "",
      rules:{
        username:[{required:true,message:'用户名不能为空',trigger:'blur'}],
        password:[{required:true,message:'密码不能为空',trigger:'blur'}]
      }
    };
  },
  methods: {
    routeregister() {
      this.$router.push("/register"); //跳转到注册
    },
    login() {
        if(this.username==''||this.password==''){
         this.$message.warning("表单项不能为空")
      }
      else
      request
        .post("/login/", {
          username: this.username,
          password: this.password
        })
        .then(res => {
          if (res.code === "111") {
            // var data = this.loginForm
            this.$store.commit("setlogin", 1);
            this.$store.commit('setnavshow',true)
            this.$store.commit('setuserType',res.userType);
            this.$store.commit("setusername", this.username);
            localStorage.setItem("token",res.token)
            this.$router.push("/mainwindow");
             this.$message({
              showClose: true,
              message: "登录成功",
              type: "success"
            });
            //change
          } else if (res.code === "222") {
            this.$message({
              showClose: true,
              message: "提示：用户名或密码错误",
              type: "warning"
            });
          } else if (res.code === "333") {
            this.$message({
              showClose: true,
              message: "用户不存在",
              type: "error"
            });
          }
        });
    }
  }
};
</script>

<style>
.loginPart {
  position: absolute;
  /*定位方式绝对定位absolute*/
  top: 50%;
  left: 50%;
  /*顶和高同时设置50%实现的是同时水平垂直居中效果*/
  transform: translate(-50%, -50%);
  /*实现块元素百分比下居中*/
  width: 300px;
  height: 300px;
  padding: 20px;
  background: rgb(255, 255, 255);
  /*背景颜色为黑色，透明度为0.8*/
  box-sizing: border-box;
  /*box-sizing设置盒子模型的解析模式为怪异盒模型，
  将border和padding划归到width范围内*/
  box-shadow: 0px 15px 25px rgba(0, 0, 0, 0.5);
  /*边框阴影  水平阴影0 垂直阴影15px 模糊25px 颜色黑色透明度0.5*/
  border-radius: 15px;
  /*边框圆角，四个角均为15px*/
}
.loginPart h2 {
  /* margin:0 0 30px;
  padding:0; */
  font-size: 20px;
  font-weight: bolder;
  color: rgba(14, 14, 14, 1);
  text-align: center;
  /*文字居中*/
}
.loginPart .inputbox {
  position: relative;
}
.loginPart .inputElement input {
  width: 100%;
  font-size: 14px;
  color: rgba(14, 14, 14, 0.5);
  letter-spacing: 1px;
  /*字符间的间距1px*/
  margin-bottom: 10px;
  border: none;
  outline: none;
  /*outline用于绘制元素周围的线
  outline：none在这里用途是将输入框的边框的线条使其消失*/
  background: transparent;
  /*背景颜色为透明*/
}
.rowDisplay{
  display:flex;
  flex-direction: row;
}
.login {
  width: 100%;
  height: 100%;
}
</style>
