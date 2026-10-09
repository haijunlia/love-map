export const moodMeta = {
  happy: { label: "开心", icon: "😊", color: "#f29b6b" },
  calm: { label: "平淡", icon: "🌿", color: "#8ab6a1" },
  sad: { label: "难过", icon: "🌧️", color: "#8ca8d8" },
  angry: { label: "生气", icon: "🔥", color: "#df7e88" }
};

export function today() {
  return new Date().toISOString().slice(0, 10);
}

export function formatDate(value) {
  if (!value) return "未设置";
  return new Date(value + "T00:00:00").toLocaleDateString("zh-CN", {
    year: "numeric",
    month: "long",
    day: "numeric"
  });
}
