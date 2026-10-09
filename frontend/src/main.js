import { createApp } from "vue";
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import "leaflet/dist/leaflet.css";
import App from "./App.vue";
import "./style.css";

createApp(App).use(ElementPlus).mount("#app");

if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("/sw.js").catch((error) => {
      console.warn("PWA Service Worker 注册失败：", error);
    });
  });
}
