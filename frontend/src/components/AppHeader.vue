<script setup>
defineProps({
  couple: { type: Object, default: null },
  activeView: { type: String, default: "dashboard" }
});

const emit = defineEmits(["navigate"]);
const menus = [
  { key: "dashboard", label: "首页", icon: "⌂" },
  { key: "diary", label: "恋爱日记", icon: "♡" },
  { key: "map", label: "我们的地图", icon: "⌖" }
];
</script>

<template>
  <header class="topbar">
    <div class="brand" @click="emit('navigate', 'dashboard')">
      <span class="brand-mark">♡</span>
      <div>
        <strong>我们的时光地图</strong>
        <small>{{ couple ? couple.nickname_a + " & " + couple.nickname_b : "把每个平凡日子收藏起来" }}</small>
      </div>
    </div>
    <nav class="main-nav">
      <button
        v-for="item in menus"
        :key="item.key"
        class="nav-button"
        :class="{ active: activeView === item.key }"
        @click="emit('navigate', item.key)"
      >
        <span>{{ item.icon }}</span>{{ item.label }}
      </button>
      <button
        class="nav-button settings-button"
        :class="{ active: activeView === 'settings' }"
        @click="emit('navigate', 'settings')"
      >
        ⚙ 设置
      </button>
    </nav>
  </header>
</template>
