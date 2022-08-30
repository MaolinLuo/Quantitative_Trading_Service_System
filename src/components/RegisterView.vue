<template>
  <div class="login">
    <img :src="imgSrc" width="100%" height="100%" alt="" />
    <div class="loginPart">

      <h2>SeuQuant用户注册</h2>
        <el-form :rules="rules">
          <div class="inputElement">
            <el-input v-model="username" placeholder="请输入用户名"></el-input>
          </div>
          <div class="inputElement">
            <el-input v-model="password1" placeholder="请输入密码 " type="password"></el-input>
          </div>
          <div class="inputElement">
            <el-input v-model="password2" placeholder="请确认密码 " type="password"></el-input>
          </div>
          <div>
            <el-button type="primary" @click="register" style="font-size:12px;">注册</el-button>
          </div>

        </el-form>
    </div>
  </div>
</template>

<script>
import request from "@/util/request";
export default {
  name: "RegisterView",
 mounted(){
   this.$store.commit("setnavshow",false)
 },
  data() {
    return {
      imgSrc: require('../assets/dollar.webp'),
      username: '',
      password1: '',
      password2:'',
       rules:{
        username:[{required:true,message:'用户名不能为空'}],
        password1:[{required:true,message:'密码不能为空'}],
        password2:[{required:true,message:'密码不能为空'}]
      }
    }
  },
  methods:{
     register () {
      console.log(this.username);
      console.log(this.password1);
      console.log(this.password2);
      if(this.username==''||this.password1==''||this.password2==''){
         this.$message.warning("表单项不能为空")
      }
      else if(this.password1===this.password2)
      {
        request.post('/register/',{
            username: this.username,
            password: this.password1
          })
          .then(res => {
            console.log(res);
            if (res.code === "111") {
              // var data = this.loginForm
            this.$message({
              showClose: true,
              message: "注册成功",
              type: "success"
            });
           this.$router.push('/login')
            }
            else if(res.code === "222"){
               this.$message({
              showClose: true,
              message: "已有该用户",
              type: "warning"
            });
            }
            
          })
      }
      else{alert('两次密码输入不一致')}
  }
  }
}
</script>

<style>
.loginPart{
  position:absolute;
  /*定位方式绝对定位absolute*/
  top:50%;
  left:50%;
  /*顶和高同时设置50%实现的是同时水平垂直居中效果*/
  transform:translate(-50%,-50%);
  /*实现块元素百分比下居中*/
  width:300px;
  height:300p;
  padding:20px;
  background: rgb(255, 255, 255);
  /*背景颜色为黑色，透明度为0.8*/
  box-sizing:border-box;
  /*box-sizing设置盒子模型的解析模式为怪异盒模型，
  将border和padding划归到width范围内*/
  box-shadow: 0px 15px 25px rgba(0,0,0,.5);
  /*边框阴影  水平阴影0 垂直阴影15px 模糊25px 颜色黑色透明度0.5*/
  border-radius:15px;
  /*边框圆角，四个角均为15px*/
}
.loginPart h2{
  /* margin:0 0 30px;
  padding:0; */
  font-size: 20px;
  font-weight: bolder;
  color: rgba(14, 14, 14, 1);
  text-align:center;
  /*文字居中*/
}
.loginPart .inputbox{
  position:relative;
}
.loginPart .inputElement input{
  width: 100%;
  font-size:14px;
  color: rgba(14, 14, 14, 0.5);
  letter-spacing: 1px;
  /*字符间的间距1px*/
  margin-bottom: 10px;
  border:none;
  outline:none;
  /*outline用于绘制元素周围的线
  outline：none在这里用途是将输入框的边框的线条使其消失*/
  background: transparent;
  /*背景颜色为透明*/
}

.login{
  width:100%;
  height:100%;
}
</style>