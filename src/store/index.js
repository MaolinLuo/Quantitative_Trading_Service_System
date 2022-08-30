import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    username:sessionStorage.getItem('username')||'',
    islogin:sessionStorage.getItem('islogin')||0,
    code:sessionStorage.getItem('setcode')||'',
    companyIndex:sessionStorage.getItem('companyIndex')||'',
    companyName:sessionStorage.getItem('companyName')||'',
    kline:sessionStorage.getItem('setkline')||'',
    res:sessionStorage.getItem('setRes')||[],
    fullloading:sessionStorage.getItem('setfullloading')||0,
    loadRise:sessionStorage.getItem('setLoadRise')||0,
    loadDragon:sessionStorage.getItem('setLoadDragon')||0,
    flagLast:1,
    incomeFlag:true,
    userType:sessionStorage.getItem('setuserType')||0,
    navshow:sessionStorage.getItem('isnavshow')||false,
   
  },
  getters: {
  },
  mutations: {
    setIncomeFlag(state,payload){
      sessionStorage.setItem('setIncomeFlag',payload)
      state.incomeFlag=payload
    },
    setFlagLast(state,payload){
      sessionStorage.setItem('setFlagLast',payload)
      state.flagLast=payload
    },
    setfullloading(state,payload){
      sessionStorage.setItem('setfullloading',payload)
      state.fullloading=payload
    },
    setLoadRise(state,payload){
      sessionStorage.setItem('setLoadRise',payload)
      state.loadRise=payload
    },
    setLoadDragon(state,payload){
      sessionStorage.setItem('setLoadDragon',payload)
      state.loadDragon=payload
    },
    setRes(state,payLoad){

      sessionStorage.setItem('setRes',payLoad)
      state.res=payLoad
      console.log("vuex res")
      console.log(state.res)
    },
    setusername(state,payload){
      sessionStorage.setItem('username',payload)
      state.username=payload
    },
    setlogin(state,payload){
      sessionStorage.setItem('islogin',payload)
      state.islogin=payload
    },
    setcode(state,payload){
      sessionStorage.setItem('setcode',payload), //change
      state.code=payload
    },
    setcompanyIndex(state,payload){
      sessionStorage.setItem('companyIndex',payload),
      state.companyIndex=payload;
    },
    setcompanyName(state,payload){
      sessionStorage.setItem('companyName',payload),
      state.companyName=payload;
    },
    setkline(state,payload){
      sessionStorage.setItem('setkline',payload),
      state.kline=payload;
    },
    setuserType(state,payload){
      sessionStorage.setItem('setuserType',payload),
      state.userType=payload
    },
    setnavshow(state,payload){
      sessionStorage.setItem('isnavshow',payload)
      state.navshow=payload

    },
    
  },
  actions: {
  },
  modules: {
  }
})
