<script setup>
import { formatDate, moodMeta } from "../composables/useLove";

defineProps({
  couple: { type: Object, default: null },
  stats: { type: Object, default: null },
  diaries: { type: Array, default: () => [] },
  places: { type: Array, default: () => [] }
});
const emit = defineEmits(["navigate"]);
</script>

<template>
  <section class="page-section">
    <div class="welcome-card">
      <div>
        <span class="eyebrow">OUR LITTLE UNIVERSE</span>
        <h1>{{ couple ? couple.nickname_a + " & " + couple.nickname_b : "欢迎来到我们的时光地图" }}</h1>
        <p>{{ couple ? "每一次相遇，都值得被好好记录。" : "先设置两个人的昵称和纪念日，再开始收藏故事吧。" }}</p>
      </div>
      <el-button v-if="!couple" type="primary" round @click="emit('navigate', 'settings')">开始设置</el-button>
    </div>

    <div class="stat-grid">
      <div class="stat-card highlight">
        <span>我们已经在一起</span>
        <strong>{{ stats?.days_together ?? "—" }}</strong>
        <small>天</small>
      </div>
      <div class="stat-card">
        <span>距离下一个纪念日</span>
        <strong>{{ stats?.next_anniversary_days ?? "—" }}</strong>
        <small>天</small>
      </div>
      <div class="stat-card">
        <span>写下的日记</span>
        <strong>{{ stats?.diary_count ?? 0 }}</strong>
        <small>篇</small>
      </div>
      <div class="stat-card">
        <span>一起去过的地方</span>
        <strong>{{ stats?.place_count ?? 0 }}</strong>
        <small>个</small>
      </div>
    </div>

    <div class="dashboard-columns">
      <section class="panel">
        <div class="panel-heading">
          <div><span class="eyebrow">MEMORIES</span><h2>最近的日记</h2></div>
          <el-button text type="primary" @click="emit('navigate', 'diary')">查看全部 →</el-button>
        </div>
        <div v-if="diaries.length" class="mini-list">
          <button v-for="diary in diaries.slice(0, 3)" :key="diary.id" class="mini-item" @click="emit('navigate', 'diary')">
            <span class="mini-icon">{{ moodMeta[diary.mood]?.icon || "♡" }}</span>
            <span><b>{{ diary.title }}</b><small>{{ formatDate(diary.diary_date) }}</small></span>
          </button>
        </div>
        <el-empty v-else description="还没有日记" />
      </section>
      <section class="panel">
        <div class="panel-heading">
          <div><span class="eyebrow">PLACES</span><h2>最近去过的地方</h2></div>
          <el-button text type="primary" @click="emit('navigate', 'map')">打开地图 →</el-button>
        </div>
        <div v-if="places.length" class="mini-list">
          <button v-for="place in places.slice(0, 3)" :key="place.id" class="mini-item" @click="emit('navigate', 'map')">
            <span class="mini-icon">⌖</span>
            <span><b>{{ place.name }}</b><small>{{ formatDate(place.visited_date) }}</small></span>
          </button>
        </div>
        <el-empty v-else description="还没有地点" />
      </section>
    </div>
  </section>
</template>
