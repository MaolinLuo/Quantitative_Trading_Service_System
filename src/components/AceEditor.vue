
<template>
  <div class="ace-container">
    <b-nav style="background-color: aliceblue">
      <b-nav-text style="margin-top: 8px;font-weight:600;margin-left:11px;">请编辑策略代码</b-nav-text>
      <b-nav-item style="margin-right:0px;margin-top:8px;font-weight:600;float:right;">
        <a
          @click="send()"
          style="text-decoration: none;font-weight:600;float:right;margin-right:10px;margin-left:10px;"
        >运行</a>
        <a
          @click="saveCode()"
          style="text-decoration: none;font-weight:600;float:right;margin-right:10px;margin-left:10px;"
        >保存</a>
        <a
          @click="userCode()"
          style="text-decoration: none;font-weight:600;float:right;margin-right:10px;margin-left:10px;"
        >我的代码</a>
        <a
          @click="templateCode()"
          style="text-decoration: none;font-weight:600;margin-right:10px;margin-left:10px;float:right;"
        >模板代码</a>
      </b-nav-item>
    </b-nav>
    <div class="ace-editor" ref="ace"></div>
  </div>
</template>
 
<script>
import request from "@/util/request";
// ace代码编辑器封装
import ace from "ace-builds";
import "ace-builds/src-noconflict/snippets/javascript";
import "ace-builds/src-noconflict/snippets/python";
import "ace-builds/src-noconflict/ext-language_tools";
import "ace-builds/src-noconflict/theme-chaos";
import "ace-builds/src-noconflict/mode-javascript";
import "ace-builds/src-noconflict/mode-python";
const wrapArray = [
  {
    name: "开启",
    value: true
  },
  {
    name: "关闭",
    value: false
  }
];

const modeArray = [
  {
    name: "Python",
    path: "ace/mode/python"
  },
  {
    name: "JavaScript",
    path: "ace/mode/javascript"
  }
];
export default {
  props: {
    value: String
  },
  mounted() {
    this.aceEditor = ace.edit(this.$refs.ace, {
      maxLines: 29,
      minLines: 29,
      fontSize: 16,
      value: this.value ? this.value : "",
      theme: this.themePath,
      mode: this.modePath,
      wrap: this.wrap,
      tabSize: 4,
      // hScrollBarAlwaysVisible: true,
      // vScrollBarAlwaysVisible: true,
      highlightGutterLine: false
    });
    // 激活自动提示
    this.aceEditor.setOptions({
      enableSnippets: true,
      enableLiveAutocompletion: true,
      enableBasicAutocompletion: true
    });
    this.aceEditor.getSession().on("change", this.change);
    window.addEventListener("resize", () => {
      this.aceEditor.resize();
    });
       
    this.getInit();
  },
  data() {
    return {
      aceEditor: null,
      toggle: false,
      wrap: true,
      themePath: "ace/theme/chaos",
      modePath: "ace/mode/python",
      modeArray: modeArray,
      wrapArray: wrapArray,
      data: [],
      trueUser: 1,
      state:''
    };
  },
  methods: {
    toggleConfigPanel() {
      this.toggle = !this.toggle;
    },
    change() {
      this.$emit("input", this.aceEditor.getSession().getValue());
    },
    handleModelPathChange(modelPath) {
      this.aceEditor.getSession().setMode(modelPath);
    },
    handleWrapChange(wrap) {
      this.aceEditor.getSession().setUseWrapMode(wrap);
    },
    saveCode() {
      
      this.data = this.aceEditor.getSession().getValue();
      request
        .post("strategy/downloadCode/", { userCode: this.data, state: "save" })
        .then(res => {
          if (res.code === "111")
            this.$message({
              showClose: true,
              message: "保存成功！",
              type: "success"
            });
          else if (res.code === "222") {
            this.$message({
              showClose: true,
              message: "状态错误",
              type: "error"
            });
          }
        });
       
    },
    send() {
      if(this.$store.state.userType===1){
      this.$store.commit("setfullloading", 1);
      this.data = this.aceEditor.getSession().getValue();
      if(this.trueUser===1) this.state='run_user'
      else this.state='run_template'
      request
        .post("strategy/downloadCode/", {userCode:this.data,state:this.state}
        )
        .then(res => {
          if (res.code === "444") {
            console.log("wo ku si");
            this.$message({
              showClose: true,
              message: "警告：代码有误",
              type: "error"
            });
          } else if (res.code === "222") {
            this.$message({
              showClose: true,
              message: "状态错误",
              type: "error"
            });
            this.$store.commit("setfullloading", 0);
            this.$router.push("/runbacktest");
          } else {
            console.log(res);
            var tempres = JSON.stringify(res);
            this.$store.commit("setRes", tempres);
            this.$store.commit("setfullloading", 0);
            this.$router.push({
              path: "/backtestdisplay",
              query: {
                name: "用户策略",
                startDate: "--",
                endDate: "--"
              }
            });
          }
        });}
        else{
          this.$message({
              showClose: true,
              message: "请先在个人中心开通VIP",
              type: "error"
            });
        }
    },
    userCode() {
     
      request
        .post("strategy/uploadCode/", { whichCode: "user"})
        .then(res => {
          this.data = res.code;
          this.aceEditor.setValue(this.data);
          this.trueUser=1;
        });
       
    },
    getInit() {
      console.log(this.$store.state.userType)
   
      this.userCode();
    },
    templateCode() {
      
      this.saveCode();
      request.post("strategy/uploadCode/", { whichCode: "template" }).then(res => {
        this.data = res.code;
        this.aceEditor.setValue(this.data);
        this.trueUser=0;
      });
    }
  }
};
</script>
 
<style lang='scss' scoped>
.ace-container {
  position: relative;
  // margin:56px 0px 4px 0px;
  .config-panel {
    position: absolute;
    right: 0;
    bottom: 0;
    width: 100%;
    height: 100%;
    overflow: scroll;
    background-color: rgb(44, 44, 44);
    z-index: 1;

    .item {
      margin: 10px auto;
      text-align: center;

      .title {
        color: white;
        margin: 0 10px;
        font-size: 14px;
      }
    }
  }
  a :hover {
    color: rgb(207, 0, 0);
    // text-shadow: 1px 3px 2px #2f6cbd, -1px -1px 1px rgb(233, 228, 228);
  }
}
</style>
