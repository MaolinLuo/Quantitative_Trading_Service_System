<template>
  <div class="company" style="60px 0px 0px 0px;">
    <!-- 左侧导航栏（参考雪球网页） -->
    <div class="left">
      <div class="bigTitle">公司概况</div>
      <div class="bigBlock">
        <li @click="getCompanyInfo()">公司简介</li>
      </div>
      <div class="bigTitle">股票交易</div>
      <div class="bigBlock">
        <li @click="getDealHref()">成交明细</li>
        <li @click=" getPriceTable()">分价表</li>
        <li @click=" getBigDealTotal()">大单统计
        </li>
        <li @click=" getBigDeal()">大宗交易</li>
      </div>
      <div class="bigTitle">公司公告</div>
      <div class="bigBlock">
        <li @click=" getNews()">
          最新公告
        </li>
        <li @click=" getYearReport()">
         年度报告
        </li>
      </div>
      <div class="bigTitle">公司运作</div>
      <div class="bigBlock">
        <li @click=" getInvestor()">
         股东大会
        </li>
        <li @click=" getIncomePercent()">
          收入构成
        </li>
        <li @click="getEvent()">
          重大事项
        </li>
      </div>
      <div class="bigTitle">财务数据</div>
      <div class="bigBlock">
        <li @click=" getPerfoemance()">
         业绩预告
        </li>
        <li @click=" getOwnerBenefitChange()">
         所有者权益变动
        </li>
      </div>
      <div class="bigTitle">研究分析</div>
      <div class="bigBlock">
        <li @click=" getDuBang()">
         杜邦分析
        </li>
        <li @click=" getSearchReport()">
          研究报告
        </li>
      </div>
    </div>
    <!-- 右侧内容主部分 -->
    <div class="main" style="display: flex;flex-direction: column;">
      <div
        class="stoclTitle"
        style="font-size: 20px; color: #0055a2; font-weight: 700;margin:10px; "
      >{{this.$store.state.companyName}}({{this.$store.state.companyIndex}})</div>
      <div style="display: flex;flex-direction: column;width:85%;overflow:auto;">
        <div style="display: flex;background-color:white" v-for="(item,key,index) in testKey" :key="index">
          <div
            style="flex:1;border: 0.5px #FFFFFF solid;padding: 5px 10px;padding: 8px;text-align:left;color: #0055a2; font-weight: 700;background-color:#F0F8FF"
          >{{key}}</div>
          <div style="flex:4;border: 0.5px #FFFFFF solid;padding: 5px 10px;">{{test[0][item]}}</div>
        </div>
      </div>
    </div>
  </div>
  <!-- </div> -->
</template>

<script>
import request from "@/util/request";
export default {
  data() {
    return {
      test: [],
      name: "",
      testKey: {
        公司ID: "company_id",
        证券代码: "code",
        公司名称: "full_name",
        公司简称: "short_name",
        A股股票代码: "main_business",
        B股股票代码: "secretary",
        H股股票代码: "h_code",
        英文名称: "fullname_en",
        英文简称: "shortname_en",
        法人代表: "legal_representative",
        注册地址: "register_location",
        办公地址: "office_address",
        邮政编码: "zipcode",
        注册资金: "register_capital",
        货币编码: "currency_id",
        货币名称: "currency",
        成立日期: "establish_date	",
        机构网址: "website",
        电子信箱: "email",
        联系电话: "contact_number",
        联系传真: "fax_number",
        主营业务: "main_business",
        经营范围: "business_scope",
        机构简介: "description",
        税务登记号: "tax_number",
        "法人营业执照号	": "license_number",
        指定信息披露报刊: "pub_newspaper	",
        指定信息披露网站: "pub_website",
        董事会秘书: "secretary",
        董秘联系电话: "secretary_number",
        董秘联系传真: "secretary_fax",
        董秘电子邮箱: "secretary_email",
        证券事务代表: "security_representative	",
        所属省份编码: "province_id",
        所属省份: "province",
        所属城市编码: "city_id",
        所属城市: "city",
        行业编码: "industry_id",
        行业一级分类: "industry_1",
        行业二级分类: "industry_2",
        会计师事务所: "cpafirm",
        律师事务所: "lawfirm",
        总经理: "ceo",
        备注: "comments"
      }
    };
  },
  created() {
    this.$store.watch(
      state => {
        return state.companyIndex;
      },
      () => {
        console.log("companyInfo watch");
        this.getCompanyInfo();
      }
    );
  },
  mounted() {
    this.getCompanyInfo();
  },
  methods: {
    getCompanyInfo() {
      console.log(this.$store.state.companyIndex);
      request
        .get("stock/companyinfo/", {
          params: { code: this.$store.state.companyIndex }
        })
        .then(res => {
          console.log("res is");
          console.log(res);
          this.test = res;
        });
    },
    getDealHref() {
      var str = "https://gu.qq.com/";
      var str1 = "/gp/detail";
      if (this.$store.state.companyIndex[0] == 6)
        window.open(
          str + "sh" + this.$store.state.companyIndex + str1,
          "_self"
        );
      else {
        window.open(
          str + "sz" + this.$store.state.companyIndex + str1,
          "_self"
        );
      }
    },
    getPriceTable() {
      var str = "https://gu.qq.com/";
      var str1 = "/gp/price";
      if (this.$store.state.companyIndex[0] == 6)
        window.open(
          str + "sh" + this.$store.state.companyIndex + str1,
          "_self"
        );
      else {
        window.open(
          str + "sz" + this.$store.state.companyIndex + str1,
          "_self"
        );
      }
    },
    getBigDealTotal() {
      var str = "https://gu.qq.com/";
      var str1 = "/gp/dadan";
      if (this.$store.state.companyIndex[0] == 6)
        window.open(
          str + "sh" + this.$store.state.companyIndex + str1,
          "_self"
        );
      else {
        window.open(
          str + "sz" + this.$store.state.companyIndex + str1,
          "_self"
        );
      }
    },
    getBigDeal() {
      var str = "https://data.eastmoney.com/dzjy/detail/";
      var str1 = ".html";
      window.open(str + this.$store.state.companyIndex + str1, "_self");
    },
    getNews() {
      if (this.$store.state.companyIndex[0] == 6) {
        var str =
          "http://www.sse.com.cn/assortment/stock/list/info/announcement/index.shtml?productId=";
        window.open(str + "sh" + this.$store.state.companyIndex, "_self");
      } else {
        var str1 =
          "http://www.szse.cn/disclosure/listed/notice/index.html?stock=";
        window.open(str1 + "sz" + this.$store.state.companyIndex, "_self");
      }
    },
    getYearReport() {
      var str =
        "http://money.finance.sina.com.cn/corp/go.php/vCB_Bulletin/stockid//page_type/ndbg.phtml";
      var str1 = "/page_type/ndbg.phtml";
      window.open(str + this.$store.state.companyIndex + str1, "_self");
    },
    getInvestor() {
      var str =
        "http://money.finance.sina.com.cn/corp/go.php/vGP_StockHolderMeeting/stockid/";
      var str1 = ".phtml";
      window.open(str + this.$store.state.companyIndex + str1, "_self");
    },
    getIncomePercent() {
      var str = "http://stockpage.10jqka.com.cn/";
      var str1 = "/operate/#analysis";
      window.open(str + this.$store.state.companyIndex + str1, "_self");
    },
    getEvent() {
      var str = "https://q.stock.sohu.com/cn/";
      var str1 = "/bw.shtml";
        window.open(
          str + this.$store.state.companyIndex + str1,
          "_self"
        );
    },
    getPerfoemance() {
         var str = "http://money.finance.sina.com.cn/corp/go.php/vFD_AchievementNotice/stockid/";
      var str1 = ".phtml";
        window.open(
          str + this.$store.state.companyIndex + str1,
          "_self"
        );
    },
    getOwnerBenefitChange() {
         var str = "http://vip.stock.finance.sina.com.cn/corp/go.php/vFD_BenifitChange/stockid/";
      var str1 = "/displaytype/4.phtml";
        window.open(
          str + this.$store.state.companyIndex + str1,
          "_self"
        );
    },
    getDuBang() {
        var str = "http://quotes.money.163.com/f10/dbfx_";
      var str1 = ".html";
        window.open(
          str+ this.$store.state.companyIndex + str1,
          "_self"
        );
    },
    getSearchReport() {
        var str = "http://stock.finance.sina.com.cn/stock/go.php/vReport_List/kind/search/index.phtml?t1=2&symbol=";
        window.open(
          str+ this.$store.state.companyIndex,
          "_self"
        );
    }
  }
};
</script>

<style scoped>
.company {
  display: flex;
  flex-direction: row;
  background-color:  #e7e9eb;
  margin: 56px 0px 0px 0px;
}
.left {
  flex: 1;
  flex-direction: column;
  height: 700px;
  background-color:  #e7e9eb;
  align-items: center;
  justify-content: center;
  text-align: center;
}
.main {
  flex: 7;
  height: 700px;
  align-items: center;
  justify-content: center;
}
.bigTitle {
  color: rgb(0, 0, 0);
  font-weight: 700;
  margin: 10px 0px 3px 0px;
  border-left: 6px solid #d75442;
}
.bigBlock {
  display: flex;
  flex-direction: column;
  margin-top: 0px;
}
li {
  display: list-item;
  list-style: none;
  line-height: 20px;
  font-size: 14px;
  color:black;
  margin-bottom: 5px;
  align-items: center;
  justify-content: center;
}
</style>