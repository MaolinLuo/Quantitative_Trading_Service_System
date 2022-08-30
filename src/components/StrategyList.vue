<template>
  <div class="mainpage-container algo-list">
    <div class="container bg-white algo-feed margin_70t">
      <h2>策略列表</h2>
       <div class="rowShow">
      <h3>量化策略均由代码实现，投资有风险，入市需谨慎!</h3>
      <a href="/runbacktest" style="font-size:24px;margin-left:130px;font-weight:600;text-decoration:none;font-size:20px">+自定义策略</a>
       </div>
      <b-card-group
        deck
        style="width: 80%; padding-left: 150px; padding-top: 10px"
        v-for="item in tableData"
        :key="item.num"
      >
        <b-card :header="item.num" header-tag="header" :title="item.title">
          <b-card-text>{{ item.text }}</b-card-text>
          <el-button type="primary" @click="huice(item.num)">回测</el-button>

          <div style="padding-top: 20px">
            <el-tag style="margin-right: 10px">{{ item.tag1 }}</el-tag>
            <el-tag style="margin-right: 10px">{{ item.tag2 }}</el-tag>
            <el-tag style="margin-right: 10px">{{ item.tag3 }}</el-tag>
            <el-tag style="margin-right: 10px" :type="[item.tag4==='会员'?'danger':'primary']">{{ item.tag4 }}</el-tag>
          </div>
        </b-card>
      </b-card-group>
    </div>

    <!-- 传统回测设定 -->
    <el-dialog
      title="回测设定"
      :visible.sync="dialogFormVisible"
      width="500px"
      lock-scroll:false
    >
      <el-form
        :model="numberValidateForm"
        ref="numberValidateForm"
        class="demo-ruleForm"
      >
      <span>回测名称</span>
        <el-form-item>
          <el-input
            v-model="backtest_id"
            placeholder="请输入此次回测的名称"
          ></el-input>
        </el-form-item>
        <span>选择股票</span>
        <el-form-item v-if="!ai_str">
          <el-tag
            :key="tag"
            v-for="tag in dynamicTags"
            closable
            :disable-transitions="false"
            @close="handleClose(tag)"
          >
            {{ tag }}
          </el-tag>
          
          <el-input
            class="input-new-tag"
            v-if="inputVisible"
            v-model="inputValue"
            ref="saveTagInput"
            size="small"
            @keyup.enter.native="handleInputConfirm()"
            @blur="handleInputConfirm()"
          >
          </el-input>
          <el-button
            v-else
            class="button-new-tag"
            size="small"
            @click="showInput()"
            >添加新股票</el-button
          >
        </el-form-item>
        <el-form-item v-if="ai_str">
          <el-input v-model="code_ai" placeholder="请输入股票代码"></el-input>
        </el-form-item>
        <span>日期设定</span>
        <el-form-item
          ><div class="block">
            <el-date-picker
              v-model="numberValidateForm.value2"
              type="daterange"
              unlink-panels
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              :picker-options="pickerOptions"
            >
            </el-date-picker></div
        ></el-form-item>
        <el-form-item v-if="ai_str"
          ><p>训练次数</p>
          <el-input-number
            v-model="epoch"
            :min="100"
            :max="300"
            label="训练次数"
          ></el-input-number>
          <p>预测步数</p>
          <el-input-number
            v-model="steps"
            :min="3"
            :max="5"
            label="预测步数"
          ></el-input-number>
          <p>涨跌幅</p>
          <el-input-number
            v-model="rate"
            :min="0.01"
            :max="0.2"
            :precision="2"
            :step="0.01"
            label="涨跌幅"
          ></el-input-number>
          <p>买卖股票数</p>
          <el-input-number
            v-model="stock_size"
            :min="10"
            :max="1000"
            label="买卖股票数"
          ></el-input-number>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm()">回测</el-button>
          <el-button
            @click="
              dialogFormVisible = false;
              ai_str = false;
            "
            >取消</el-button
          >
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
import request from "@/util/request";

export default {
  name: "StrategyList",
  data() {
    return {
      tableData: [],
      backtest_id:'',
      dialogFormVisible: false,
      pickerOptions: {
        shortcuts: [
          {
            text: "最近一年",
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 365);
              picker.$emit("pick", [start, end]);
            },
          },
          {
            text: "最近两年",
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 730);
              picker.$emit("pick", [start, end]);
            },
          },
        ],
      },
      numberValidateForm: {
        value2: "",
      },
      str_num: 0,
      ai_str: 0,
      epoch: 150,
      steps: 3,
      rate: 0.03,
      stock_size: 100,
      dynamicTags: ["000001.SZ", "000002.SZ", "000004.SZ", "000005.SZ"],
      inputVisible: false,
      inputValue: "",
      code_ai: "002169.SZ",
    };
  },
  mounted() {
    request.get("/strategy/list/").then((res) => {
      // console.log(res);
      this.tableData = res;
    });
  },
  methods: {
    huice(num) {
      this.str_num = num;
      if (num == 1 || num == 2 || num == 3 || num == 4 ||num==5) {
        this.dialogFormVisible = true;
        this.ai_str = false;
      } else {
        this.ai_str = true;
        this.dialogFormVisible = true;
      }
    },
    format(date) {
      var y = date.getFullYear();
      var m = date.getMonth() + 1;
      m = m < 10 ? "0" + m : m;
      var d = date.getDate();
      d = d < 10 ? "0" + d : d;
      return y + "-" + m + "-" + d;
    },
    submitForm() {
      // console.log(this.numberValidateForm.value2);
      if (
        this.str_num == 1 ||
        this.str_num == 2 ||
        this.str_num == 3 ||
        this.str_num == 4 ||
        this.str_num==5
      ) {
       
        this.$router.push({
          path: "/backtestdisplay",
          query: {
            backtest_id: this.backtest_id,
            name: this.tableData[this.str_num - 1].title,
            startDate: this.format(this.numberValidateForm.value2[0]),
            endDate: this.format(this.numberValidateForm.value2[1]),
            codes: this.dynamicTags,
          },
        });
      } else {
         if(this.$store.state.userType==0){
          this.$message({
              showClose: true,
              message: "会员专享策略",
              type: "danger"
            });
        }
        else{this.$router.push({
          path: "/backtestdisplay",
          query: {
            backtest_id: this.backtest_id,
            name: this.tableData[this.str_num - 1].title,
            startDate: this.format(this.numberValidateForm.value2[0]),
            endDate: this.format(this.numberValidateForm.value2[1]),
            epoch: this.epoch,
            steps: this.steps,
            rate: this.rate,
            stock_size: this.stock_size,
            code_ai: this.code_ai,
          },
        });
      }}
    },
    handleClose(tag) {
      this.dynamicTags.splice(this.dynamicTags.indexOf(tag), 1);
    },
    showInput() {
      this.inputVisible = true;
      this.$nextTick(() => {
        this.$refs.saveTagInput.$refs.input.focus();
      });
    },
    handleInputConfirm() {
      let inputValue = this.inputValue;
      if (inputValue) {
        this.dynamicTags.push(inputValue);
      }
      this.inputVisible = false;
      this.inputValue = "";
    },
  },
};
</script>

<style scoped>
.algo-toolbar {
  height: auto;
  border: none;
}
.block {
  display: block;
}

.clear {
  clear: both;
}
.index-list .algo-toolbar .algo-title {
  font-size: 18px;
}
.backtest-header {
  position: relative;
  top: 7px !important;
}
.fleft {
  float: left;
}
.mainpage-container.algo-list {
  padding: 10px;
}

.mainpage-container {
  min-height: 450px;
}
.margin_70t {
  margin-top: 70px;
}

.bg-white {
  background-color: #fff;
}
.algo-feed {
  min-height: 400px;
}
.mainpage-container.algo-list .container {
  border: none;
  width: 1180px;
}

.row-box .el-card {
  min-width: 100%;
  height: 100%;
  margin-right: 20px;
  border: 0px;
  box-shadow: 0 2px 12px 0 rgb(0 0 0 / 10%);
}
.rowShow{
  display: flex;
  flex-direction: row;
}
h2 {
  height: 21px;
  line-height: 21px;
  font-weight: 700;
  border-left: 6px solid #528fcc;
  padding-left: 10px;
  font-size: 18px;
  overflow: hidden;
}
h3 {
  border-left: 6px solid #b70822;
  padding-left: 10px;
}
.el-tag + .el-tag {
  margin-left: 10px;
}
.button-new-tag {
  margin-left: 10px;
  height: 32px;
  line-height: 30px;
  padding-top: 0;
  padding-bottom: 0;
}
.input-new-tag {
  width: 90px;
  margin-left: 10px;
  vertical-align: bottom;
}
</style>