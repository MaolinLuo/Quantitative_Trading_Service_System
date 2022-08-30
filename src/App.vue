<template>
  <div id="app">
<TopNavigator></TopNavigator>
<router-view></router-view>
 <FooterBar style="align-self:flex-end"></FooterBar>
  </div>
</template>

<style>
html,body,#app{
  height: 100%;
  margin: 0;
  padding: 0;
}
</style>
<script>
import TopNavigator from "@/components/TopNavigator";
import FooterBar from "@/components/FooterBar";
export default {
  components:{
    TopNavigator,
    FooterBar,
  },
}
</script>