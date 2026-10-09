<script setup>
defineProps({
  photos: { type: Array, default: () => [] }
});
</script>

<template>
  <div v-if="photos.length" class="photo-grid">
    <a v-for="photo in photos" :key="photo.id" :href="photo.url" target="_blank" rel="noreferrer">
      <img :src="photo.url" alt="时光照片" loading="lazy" />
    </a>
  </div>
</template>
