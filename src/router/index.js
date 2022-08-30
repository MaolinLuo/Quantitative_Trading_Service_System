import Vue from "vue";
import VueRouter from "vue-router";

const LoginView = () => import("@/components/LoginView");
const RegisterView = () => import("@/components/RegisterView");
const MainWindowVeiw = () => import("@/components/MainWindowView");
const StrategyList = () => import("@/components/StrategyList");
const StockDisplay = () => import("@/components/StockDisplay");
const kline = () => import("@/components/kline");
const CompanyInfo = () => import("@/components/CompanyInfo");
const UserInterface = () => import("@/components/UserInterface");
const TestDemo=()=>import("@/components/TestDemo")
const RunBacktest=()=>import("@/components/RunBacktest")
const Display=()=>import("@/components/BackTest/Display")
const BackTestHistory=()=>import("@/components/BackTest/BackTestHistory")
Vue.use(VueRouter);

const route = [
  {
    path:"/runbacktest",
    component:RunBacktest,
  },
  {
    path:"/backtesthistory",
    component:BackTestHistory,
  },
  {
    path: "/testdemo",
    component: TestDemo,
  },
  {
    path: "/userinterface",
    component: UserInterface,
  },
  {
    path: "",
    redirect: "/login",
  },
  {
    path: "/login",

    component: LoginView,
  },
  {
    path: "/register",
    component: RegisterView,
  },
  {
    path: "/mainwindow",
    component: MainWindowVeiw,
  },
  {
    path: "/strategylist",
    component: StrategyList,
  },
  {
    path: "/backtestdisplay",
    component:Display,
  },
  {
    path: "/stockdisplay",
    component: StockDisplay,
    children: [
      {
        path: "",
        component: kline,
      },
    ],
  },
  {
    path: "/companyinfo",
    component: CompanyInfo,
  },
];

export default new VueRouter({
  routes: route,
  mode: "history",
});

export { route };
