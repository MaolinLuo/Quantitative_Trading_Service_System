<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <div style="height:100%; padding-top: 55px">
    <!-- 次级导航栏 -->
    <b-nav style="background-color: aliceblue">
      <b-nav-item @click="turnPage()" style="margin-top: 8px">
        <i class="el-icon-arrow-left"></i>
      </b-nav-item>
      <b-nav-item style="margin-top: 8px">
        <span v-text="name_strategy"></span>
      </b-nav-item>
      <b-nav-text style="margin-top: 8px">回测详情</b-nav-text>
      <b-nav-text style="margin-left: auto; margin-right: 1px; margin-top: 8px">时间设置:</b-nav-text>
      <b-nav-item style="margin-top: 8px">
        <span v-text="startDate"></span>
      </b-nav-item>
      <b-nav-text style="margin-top: 8px">到</b-nav-text>
      <b-nav-item style="margin-top: 8px; margin-right: 20px">
        <span v-text="endDate"></span>
      </b-nav-item>
      <b-nav-text style="margin-top: 8px">本金:</b-nav-text>
      <b-nav-item style="margin-top: 8px">
        <span>￥1000000</span>
      </b-nav-item>
    </b-nav>
    <!-- 左侧导航栏+主要界面 -->
    <b-tabs content-class="mt-3" justified fill vertical style="height:450px;">
      <b-tab active>
        <template #title>
          <span class="icontab0">收益概述</span>
        </template>
        <!-- <p>I'm the 收益概述 tab</p> -->
        <income
          title="收益概述"
          :name="this.name_strategy"
          :startDate="this.startDate"
          :endDate="this.endDate"
          :epoch="this.epoch"
          :steps="this.steps"
          :rate="this.rate"
          :stock_size="this.stock_size"
          :codes="this.codes"
          :code_ai="this.code_ai"
          :backtest_id="this.backtest_id"
        ></income>
      </b-tab>
      <!-- <b-tab v-model="trade"> -->
      <b-tab :disabled="this.$store.state.incomeFlag">
        <template #title>
          <span class="icontab1">交易详情</span>
        </template>
        <TradeList title="交易详情"></TradeList>
      </b-tab>
      <!-- <b-tab v-model="hold"> -->
      <b-tab :disabled="this.$store.state.incomeFlag">
        <template #title>
          <span class="icontab2">每日持仓&收益</span>
        </template>
        <HoldList title="每日持仓&收益"></HoldList>
      </b-tab>
    </b-tabs>
  </div>
</template>

<script>
import income from "./income.vue";
import TradeList from "./TradeList.vue";
import HoldList from "./HoldList.vue";

export default {
  data() {
    return {
      name_strategy: "",
      startDate: "",
      endDate: "",
      epoch: 0,
      steps: 0,
      rate: 0,
      stock_size: 0,
      code_ai: "",
      codes: [],
      backtest_id: ""
    };
  },
  created() {
    this.name_strategy = this.$route.query.name;
    this.startDate = this.$route.query.startDate;
    this.endDate = this.$route.query.endDate;
    this.epoch = this.$route.query.epoch;
    this.steps = this.$route.query.steps;
    this.rate = this.$route.query.rate;
    this.stock_size = this.$route.query.stock_size;
    this.code_ai = this.$route.query.code_ai;
    this.codes = this.$route.query.codes;
    this.backtest_id = this.$route.query.backtest_id;
    this.$store.watch(
      state => {
        return state.incomeFlag;
      },
    );
  },
  components: {
    income,
    TradeList,
    HoldList
  },
  methods: {
    turnPage() {
      if (this.$store.state.flagLast === 1) {
        this.$router.push("/strategylist");
      } else this.$router.push("/backtesthistory");
    }
  },
};
</script>
<style scoped>
.icontab0 {
  padding: 0px 0px 0px 23px;
  background-image: url(../../../src/assets/icons/money.png);
  background-size: 20px 20px;
  background-repeat: no-repeat;
}
.icontab1 {
  padding: 0px 0px 0px 23px;
  background-image: url(../../../src/assets/icons/page.png);
  background-size: 20px 20px;
  background-repeat: no-repeat;
  pointer-events: auto;
}
.icontab2 {
  padding: 0px 0px 0px 23px;
  background-image: url(../../../src/assets/icons/bulb.png);
  background-size: 20px 20px;
  background-repeat: no-repeat;
  pointer-events: auto;
}
.icontab3 {
  padding: 0px 0px 0px 23px;
  background-image: url(../../../src/assets/icons/database.png);
  background-size: 20px 20px;
  background-repeat: no-repeat;
}
</style>