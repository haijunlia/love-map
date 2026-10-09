<script setup>
import { onBeforeUnmount, onMounted, ref } from "vue";

const deferredPrompt = ref(null);
const canInstall = ref(false);

function capturePrompt(event) {
  event.preventDefault();
  deferredPrompt.value = event;
  canInstall.value = true;
}

function installed() {
  deferredPrompt.value = null;
  canInstall.value = false;
}

async function install() {
  if (!deferredPrompt.value) return;
  deferredPrompt.value.prompt();
  await deferredPrompt.value.userChoice;
  installed();
}

onMounted(() => {
  window.addEventListener("beforeinstallprompt", capturePrompt);
  window.addEventListener("appinstalled", installed);
});

onBeforeUnmount(() => {
  window.removeEventListener("beforeinstallprompt", capturePrompt);
  window.removeEventListener("appinstalled", installed);
});
</script>

<template>
  <el-button v-if="canInstall" class="install-button" size="small" round @click="install">
    安装到手机
  </el-button>
</template>
