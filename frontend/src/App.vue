<script setup>
import { onMounted, ref } from "vue";
import { ElMessage } from "element-plus";
import AppHeader from "./components/AppHeader.vue";
import DashboardView from "./views/DashboardView.vue";
import DiaryView from "./views/DiaryView.vue";
import MapPageView from "./views/MapPageView.vue";
import SettingsView from "./views/SettingsView.vue";
import { api } from "./services/api";

const activeView = ref("dashboard");
const couple = ref(null);
const stats = ref(null);
const diaries = ref([]);
const places = ref([]);
const loading = ref(true);
const error = ref("");

async function loadData() {
  loading.value = true;
  error.value = "";
  try {
    const results = await Promise.all([
      api.getCouple(),
      api.getStats(),
      api.listDiaries(),
      api.listPlaces()
    ]);
    couple.value = results[0];
    stats.value = results[1];
    diaries.value = results[2];
    places.value = results[3];
    if (!couple.value) activeView.value = "settings";
  } catch (requestError) {
    error.value = requestError.message;
  } finally {
    loading.value = false;
  }
}

async function refreshData() {
  await loadData();
}

function handleSaved(saved) {
  couple.value = saved;
  activeView.value = "dashboard";
  refreshData();
}

onMounted(loadData);
</script>

<template>
  <div class="app-shell">
    <AppHeader :couple="couple" :active-view="activeView" @navigate="activeView = $event" />
    <main v-loading="loading" class="app-main">
      <el-alert v-if="error" :title="error + '。请确认后端已经启动。'" type="error" show-icon closable class="global-alert" />
      <DashboardView v-if="activeView === 'dashboard'" :couple="couple" :stats="stats" :diaries="diaries" :places="places" @navigate="activeView = $event" />
      <DiaryView v-else-if="activeView === 'diary'" :diaries="diaries" @changed="refreshData" />
      <MapPageView v-else-if="activeView === 'map'" :places="places" :diaries="diaries" @changed="refreshData" />
      <SettingsView v-else :couple="couple" @saved="handleSaved" />
    </main>
    <footer class="app-footer">把平凡的日子，过成值得回看的故事。</footer>
  </div>
</template>
