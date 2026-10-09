<script setup>
import { reactive, ref, watch } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import { api } from "../services/api";
import DiaryCard from "../components/DiaryCard.vue";
import DiaryForm from "../components/DiaryForm.vue";

const props = defineProps({
  diaries: { type: Array, default: () => [] }
});
const emit = defineEmits(["changed"]);
const list = ref([...props.diaries]);
const dialogVisible = ref(false);
const editing = ref(null);
const filters = reactive({ mood: "", start_date: "", end_date: "" });
const dateRange = ref([]);
const loading = ref(false);

watch(() => props.diaries, (value) => { list.value = [...value]; });

async function refresh() {
  loading.value = true;
  try {
    list.value = await api.listDiaries(filters);
  } finally {
    loading.value = false;
  }
}

function applyDateRange(value) {
  filters.start_date = value?.[0] || "";
  filters.end_date = value?.[1] || "";
  refresh();
}

function openCreate() {
  editing.value = null;
  dialogVisible.value = true;
}

function openEdit(diary) {
  editing.value = diary;
  dialogVisible.value = true;
}

async function saveDiary(payload) {
  try {
    const saved = editing.value
      ? await api.updateDiary(editing.value.id, payload.data)
      : await api.createDiary(payload.data);
    for (const file of payload.files) {
      await api.uploadDiaryPhoto(saved.id, file);
    }
    ElMessage.success(editing.value ? "日记已更新" : "日记已保存");
    dialogVisible.value = false;
    emit("changed");
    await refresh();
  } catch (error) {
    ElMessage.error(error.message);
  }
}

async function removeDiary(diary) {
  try {
    await ElMessageBox.confirm("删除后无法恢复，确定要删除这篇日记吗？", "确认删除", { type: "warning" });
    await api.deleteDiary(diary.id);
    ElMessage.success("日记已删除");
    emit("changed");
    await refresh();
  } catch (error) {
    if (error !== "cancel" && error !== "close") ElMessage.error(error.message);
  }
}
</script>

<template>
  <section class="page-section">
    <div class="page-title-row">
      <div><span class="eyebrow">OUR DIARY</span><h1>恋爱日记</h1><p>把今天的心情和小事，留给未来的我们。</p></div>
      <el-button type="primary" round @click="openCreate">＋ 写一篇日记</el-button>
    </div>
    <div class="filter-bar panel">
      <el-select v-model="filters.mood" clearable placeholder="按心情筛选" @change="refresh">
        <el-option label="😊 开心" value="happy" />
        <el-option label="🌿 平淡" value="calm" />
        <el-option label="🌧️ 难过" value="sad" />
        <el-option label="🔥 生气" value="angry" />
      </el-select>
      <el-date-picker v-model="dateRange" type="daterange" value-format="YYYY-MM-DD" range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期" @change="applyDateRange" />
      <el-button @click="filters.mood = ''; dateRange = []; filters.start_date = ''; filters.end_date = ''; refresh()">重置筛选</el-button>
    </div>
    <div v-loading="loading" class="timeline">
      <DiaryCard v-for="diary in list" :key="diary.id" :diary="diary" @edit="openEdit" @delete="removeDiary" />
      <el-empty v-if="!loading && !list.length" description="还没有符合条件的日记" />
    </div>
    <el-dialog v-model="dialogVisible" :title="editing ? '编辑日记' : '写一篇新日记'" width="680px" destroy-on-close>
      <DiaryForm :diary="editing" @submit="saveDiary" @cancel="dialogVisible = false" />
    </el-dialog>
  </section>
</template>
