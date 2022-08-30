<template>
  <div ref="main" style="height: 500px;width: 100%;padding-top: 0px">

  </div>
</template>

<script>
import * as echarts from "echarts";
import request from "@/util/request";

export default {
  name: "KLine",
  data() {
    return{
      stockdata:[[]],
      datedata:[],
      ma5data:[],
      ma10data:[],
      ma20data:[],
      ma30data:[],
      voldata:[],
    }
  },
  created() {
    this.$store.watch((state)=>{
      return state.code
    },()=>{
      this.loadhistory()
     console.log("kline watch")
    })
    console.log("kline create")
  },
  mounted(){
    this.loadhistory()
  },
  methods:{
    loadhistory(){
      var chartDom = this.$refs.main;
      var charts = echarts.init(chartDom);
      charts.showLoading();
      request.get('/stock/kline/',{params:{code:this.$store.state.code}}).then(res=>{
        if(res.code==="222")
        {
           this.$message({message: '无效股票代码',type: 'warning'});
           this.$router.push('/mainwindow')
        }
        else if(res)
        {
          this.setcharts(res,charts);
        }
      }).catch(e=>{console.log(e)})
    },
    setcharts(res,charts){
      this.stockdata=[[]]
      this.voldata=[]
      this.datedata=[]
      this.ma5data=[]
      this.ma10data=[]
      this.ma20data=[]
      this.ma30data=[]
      var arr=Object.keys(res.close)
      for(let i=0;i<arr.length;i++){
        this.datedata[i]=res['trade_date'][i];
        this.ma5data[i]=res.ma5[i];
        this.ma10data[i]=res.ma10[i];
        this.ma20data[i]=res.ma20[i];
        this.ma30data[i]=res.ma30[i];
        this.voldata.push([i,res.vol[i],res.open[i]>res.close[i]?1:-1])
        this.stockdata[i]=[];
        for(let j=0;j<4;j++){
          var temp=[];
          temp[0]=res.open[i];
          temp[1]=res.close[i];
          temp[2]=res.low[i];
          temp[3]=res.high[i];
          this.stockdata[i][j]=temp[j]}
      }
      var option = {
        title:{

          text:this.$store.state.code},
        legend: {
          
          data: ['日K','MA5', 'MA10', 'MA20', 'MA30']
        },
        grid: [
          {
            left: '10%',
            right: '8%',
            height: '50%'
          },
          {
            left: '10%',
            right: '8.5%',
            top: '63%',
            height: '14%'
          }
        ],
        axisPointer: {
          link: [
            {
              xAxisIndex: 'all'
            }
          ],
          label: {
            backgroundColor: '#777'
          }
        },
        xAxis: [
          {
            type: 'category',
            data: this.datedata,
            boundaryGap: false,
            axisLine: { onZero: false },
            splitLine: { show: false },
            min: 'dataMin',
            max: 'dataMax',
            axisPointer: {
              z: 100
            }
          },
          {
            type: 'category',
            gridIndex: 1,
         data:this.datedata,
            boundaryGap: false,
            axisLine: { onZero: false },
            axisTick: { show: false },
            splitLine: { show: false },
            axisLabel: { show: false },
            min: 'dataMin',
            max: 'dataMax'
          }
        ],

        yAxis: [
          {
            scale: true,
            splitArea: {
              show: true
            }
          },
          {

            scale: true,
            gridIndex: 1,
            splitNumber: 2,
            axisLabel: { show: false },
            axisLine: { show: false },
            axisTick: { show: false },
            splitLine: { show: false }
          }
        ],
        dataZoom: [
          {
            type: 'inside',
            xAxisIndex: [0, 1],
            start: 80,
            end: 100
          },
          {
            show: true,
            xAxisIndex: [0, 1],
            type: 'slider',
            top: '78%',
            start: 80,
            end: 100
          }
        ],
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross'
          },
          borderWidth: 1,
          borderColor: '#ccc',
          padding: 10,
          position: function (pos, params, el, elRect, size) {
            const obj = {
              top: 10
            };
            obj[['left', 'right'][+(pos[0] < size.viewSize[0] / 2)]] = 30;
            return obj;
          }
        },
         visualMap: {
          show: false,
          seriesIndex: 5,
          dimension: 2,
          pieces: [
            {
              value: 1,
              color: '#0CF49B'
            },
            {
              value: -1,
              color: '#FD1050',
            }
          ]
        },

        series: [
          {
            name:'日K',
            type: 'candlestick',
            data:this.stockdata,
               itemStyle: {
              normal: {
                color: '#FD1050',
                color0: '#0CF49B',
                borderColor: '#FD1050',
                borderColor0: '#0CF49B'
              }
            },

          },
          {
            name: 'MA5',
            type: 'line',
            data: this.ma5data,
            smooth: true,
            showSymbol:false,
            lineStyle: {
              opacity: 0.5
            }
          },
          {
            name: 'MA10',
            type: 'line',
            data: this.ma10data,
            smooth: true,
            showSymbol:false,
            lineStyle: {
              opacity: 0.5
            }
          },
          {
            name: 'MA20',
            type: 'line',
            data: this.ma20data,
            smooth: true,
             showSymbol:false,
            lineStyle: {
              opacity: 0.5
            }
          },
          {
            name: 'MA30',
            type: 'line',
            data: this.ma30data,
            smooth: true,
             showSymbol:false,
            lineStyle: {
              opacity: 0.5
            }
          },

          {
            name: 'Volume',
            type: 'bar',
            xAxisIndex: 1,
            yAxisIndex: 1,
            data: this.voldata
          }

        ]
      };
      charts.hideLoading();
      charts.clear()
      charts.resize()
      charts.setOption(option,true);

    }
  }
}
</script>

<style scoped>

</style>