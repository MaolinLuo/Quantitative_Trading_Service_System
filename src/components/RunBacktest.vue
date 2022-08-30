<template>
  <div class="allComponents">
    <div class="leftSize">
      <AceEditor></AceEditor>
    </div>
    <div class="sx"></div>
    <div class="rightSize">
      <!-- <MdText></MdText> -->
      <VueMarkdown class="markdown" :source="md">{{md}}</VueMarkdown>
    </div>
  </div>
</template>
<script>
// import MdText from "@/components/MdText";
import { Loading } from "element-ui";
import request from "@/util/request";
import VueMarkdown from "vue-markdown";

export default {
  components: {
    //   MdText,
    VueMarkdown
  },
  data() {
    return {
      md: ""
    };
  },
  created(){
      this.$store.watch((state)=>{
      return state.fullloading
    },()=>{
      this.controlLoading()
    })
  },
  mounted(){
    if(this.$store.state.userType==0){this.$message({
              showClose: true,
              message: "非VIP用户不能运行",
              type: "error"
            });}
    this.getMarkDown();
  },
  methods:{
    getMarkDown() {
      request.post("strategy/uploadMd/").then(res => {
        this.md = res.Md;
      });
    },
    // 此页面加载动画
    controlLoading() {
      if (this.$store.state.fullloading==0) {
          // 以服务的方式调用的 Loading 需要异步关闭
          this.loading.close();
      } else if (this.$store.state.fullloading==1) {
        this.loading=Loading.service({ fullscreen: true, text: "拼命运行中"});
      }
    }
  }
};
</script>
<style scoped>
.allComponents {
  margin: 56px 0px 0px 0px;
  display: flex;
  flex-direction: row;
}
.leftSize {
  width: 50%;
}
.sx {
  width: 5px;
  height: 635px;
  background: darkgray;
  margin-left: 5px;
  margin-right: 5px;
}
.rightSize {
  width: 50%;
  height: 600px;
  overflow: auto;
}
@import "github-markdown-css/github-markdown.css";
@media (max-width: 767px) {
  .markdown-body {
    padding: 0px;
  }
}
</style>