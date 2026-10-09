<script setup>
import { formatDate, moodMeta } from "../composables/useLove";
import PhotoGrid from "./PhotoGrid.vue";

defineProps({
  diary: { type: Object, required: true }
});

const emit = defineEmits(["edit", "delete"]);
</script>

<template>
  <article class="diary-card">
    <div class="diary-date">
      <span>{{ formatDate(diary.diary_date) }}</span>
      <b>{{ moodMeta[diary.mood]?.icon || "♡" }}</b>
    </div>
    <div class="diary-card-body">
      <div class="card-heading">
        <div>
          <span class="eyebrow">{{ moodMeta[diary.mood]?.label || diary.mood }}</span>
          <h3>{{ diary.title }}</h3>
        </div>
        <div class="card-actions">
          <el-button text @click="emit('edit', diary)">编辑</el-button>
          <el-button text type="danger" @click="emit('delete', diary)">删除</el-button>
        </div>
      </div>
      <p class="diary-content">{{ diary.content }}</p>
      <PhotoGrid :photos="diary.photos" />
    </div>
  </article>
</template>
