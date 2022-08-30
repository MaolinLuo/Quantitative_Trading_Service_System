<template>
  <div style="width: 100%;height: 100%">
    <div class="toolBar">
      <div class="left inline-block" style="margin-left:11px;">
        <el-button class="btn" type="primary" @click="send()">提交</el-button>
      </div>
    </div>
    <mavon-editor
      v-model="value"
      @save="save"
      :toolbarsFlag="!readOnly"
      :defaultOpen="readOnly?'preview':'edit'"
      :ishljs="true"
      :subfield="readOnly"
      :editable="readOnly"
      @imgAdd="imgAdd"
      ref="md"
    />
  </div>
</template>
 
<script>
import request from "@/util/request";
import { mavonEditor } from "mavon-editor";
import "mavon-editor/dist/css/index.css";
export default {
  name: "HelloWorld",
  components: {
    mavonEditor
  },
  props: {
    markContent: {
      type: String,
      default: ""
    },
    alikey: {
      type: String,
      default: ""
    },
    alisecret: {
      type: String,
      default: ""
    },
    readOnly: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      value: "",
      token: null
    };
  },
  mounted() {
    this.value = this.markContent;
  },
  methods: {
    save(value, render) {
      this.$emit("save", value, render);
    },
    send() {
      request.post().then(res => {
        console.log(res);
      });
    }
    // imgAdd(pos,file){
    //   // 第一步.将图片上传到服务器.
    //   let formdata = new FormData();
    //   request('',{data: formdata,headers: { 'Content-Type': 'multipart/form-data', "Signature":this.token}}
    //   ).then(res => {
    //     // 第二步.将返回的url替换到文本原位置![...](./0) -> ![...](url)
    //     /**
    //      * $vm 指为mavonEditor实例，可以通过如下两种方式获取
    //      * 1. 通过引入对象获取: `import {mavonEditor} from ...` 等方式引入后，`$vm`为`mavonEditor`
    //      * 2. 通过$refs获取: html声明ref : `<mavon-editor ref=md ></mavon-editor>，`$vm`为 `this.$refs.md`
    //      */
    //     let url=res.data.data[0].url;
    //     console.log(this.$refs.md);
    //     console.log(file);
    //     this.$refs.md.$img2Url(pos, url);
    //   })
    // }
  }
};
</script>
 
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>