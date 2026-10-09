<script setup>
import { onBeforeUnmount, onMounted, ref, watch } from "vue";
import L from "leaflet";

const props = defineProps({
  places: { type: Array, default: () => [] }
});
const emit = defineEmits(["pick", "select"]);
const mapElement = ref(null);
let map;
let markerLayer;

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (char) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#039;"
  }[char]));
}

function renderMarkers() {
  if (!map || !markerLayer) return;
  markerLayer.clearLayers();
  props.places.forEach((place, index) => {
    const icon = L.divIcon({
      className: "love-map-marker",
      html: "<span>" + (index + 1) + "</span>",
      iconSize: [36, 36],
      iconAnchor: [18, 34]
    });
    const marker = L.marker([place.latitude, place.longitude], { icon });
    marker.bindPopup(
      "<strong>" + escapeHtml(place.name) + "</strong><br>" +
      escapeHtml(place.visited_date) +
      (place.diary_title ? "<br>" + escapeHtml(place.diary_title) : "")
    );
    marker.on("click", () => emit("select", place));
    markerLayer.addLayer(marker);
  });
}

onMounted(() => {
  map = L.map(mapElement.value).setView([35.8, 104.1], 4);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "&copy; OpenStreetMap contributors"
  }).addTo(map);
  markerLayer = L.layerGroup().addTo(map);
  map.on("click", (event) => {
    emit("pick", {
      latitude: Number(event.latlng.lat.toFixed(6)),
      longitude: Number(event.latlng.lng.toFixed(6))
    });
  });
  renderMarkers();
});

watch(() => props.places, renderMarkers, { deep: true });

onBeforeUnmount(() => {
  if (map) map.remove();
});
</script>

<template>
  <div ref="mapElement" class="map-canvas"></div>
</template>
