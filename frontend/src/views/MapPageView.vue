<script setup>
import { reactive, ref, watch } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import { api } from "../services/api";
import { today, formatDate } from "../composables/useLove";
import MapView from "../components/MapView.vue";
import PhotoGrid from "../components/PhotoGrid.vue";

const props = defineProps({
  places: { type: Array, default: () => [] },
  diaries: { type: Array, default: () => [] }
});
const emit = defineEmits(["changed"]);
const list = ref([...props.places]);
const dialogVisible = ref(false);
const editing = ref(null);
const picked = ref(null);
const files = ref([]);
const form = reactive({ name: "", latitude: null, longitude: null, visited_date: today(), diary_id: null });

watch(() => props.places, (value) => { list.value = [...value]; });

function resetForm(position = null) {
  editing.value = null;
  picked.value = position;
  form.name = "";
  form.latitude = position?.latitude ?? null;
  form.longitude = position?.longitude ?? null;
  form.visited_date = today();
  form.diary_id = null;
  files.value = [];
}

function startAdd(position = null) {
  resetForm(position);
  dialogVisible.value = true;
}

function editPlace(place) {
  editing.value = place;
  picked.value = { latitude: place.latitude, longitude: place.longitude };
  form.name = place.name;
  form.latitude = place.latitude;
  form.longitude = place.longitude;
  form.visited_date = place.visited_date;
  form.diary_id = place.diary_id;
  files.value = [];
  dialogVisible.value = true;
}

function chooseFiles(event) {
  files.value = Array.from(event.target.files || []);
}

async function savePlace() {
  if (!form.name || form.latitude === null || form.longitude === null) {
    ElMessage.warning("请点击地图选择位置，并填写地点名称");
    return;
  }
  try {
    const data = { ...form };
    const saved = editing.value
      ? await api.updatePlace(editing.value.id, data)
      : await api.createPlace(data);
    for (const file of files.value) {
      await api.uploadPlacePhoto(saved.id, file);
    }
    ElMessage.success(editing.value ? "地点已更新" : "地点已保存");
    dialogVisible.value = false;
    emit("changed");
    list.value = await api.listPlaces();
  } catch (error) {
    ElMessage.error(error.message);
  }
}

async function removePlace(place) {
  try {
    await ElMessageBox.confirm("删除这个地点吗？", "确认删除", { type: "warning" });
    await api.deletePlace(place.id);
    ElMessage.success("地点已删除");
    emit("changed");
    list.value = await api.listPlaces();
  } catch (error) {
    if (error !== "cancel" && error !== "close") ElMessage.error(error.message);
  }
}
</script>

<template>
  <section class="page-section map-page">
    <div class="page-title-row">
      <div><span class="eyebrow">OUR MAP</span><h1>我们的地图</h1><p>点击地图上的任意位置，记录一起去过的地方。</p></div>
      <el-button type="primary" round @click="startAdd()">＋ 添加地点</el-button>
    </div>
    <div class="map-layout">
      <div class="panel map-panel">
        <MapView :places="list" @pick="startAdd" @select="editPlace" />
      </div>
      <aside class="panel place-sidebar">
        <div class="panel-heading"><div><span class="eyebrow">MEMORY SPOTS</span><h2>去过的地方</h2></div><span class="count-badge">{{ list.length }}</span></div>
        <div v-if="list.length" class="place-list">
          <button v-for="(place, index) in list" :key="place.id" class="place-item" @click="editPlace(place)">
            <span class="place-number">{{ index + 1 }}</span>
            <span><b>{{ place.name }}</b><small>{{ formatDate(place.visited_date) }}</small></span>
          </button>
        </div>
        <el-empty v-else description="在地图上点一下，添加第一个地方" />
      </aside>
    </div>
    <el-dialog v-model="dialogVisible" :title="editing ? '编辑地点' : '添加一个去过的地方'" width="520px" destroy-on-close>
      <el-form label-position="top">
        <el-form-item label="地点名称"><el-input v-model="form.name" placeholder="例如：杭州西湖" /></el-form-item>
        <div class="form-two-columns">
          <el-form-item label="纬度"><el-input-number v-model="form.latitude" :precision="6" :step="0.0001" controls-position="right" /></el-form-item>
          <el-form-item label="经度"><el-input-number v-model="form.longitude" :precision="6" :step="0.0001" controls-position="right" /></el-form-item>
        </div>
        <el-form-item label="去过的日期"><el-date-picker v-model="form.visited_date" type="date" value-format="YYYY-MM-DD" /></el-form-item>
        <el-form-item label="关联日记"><el-select v-model="form.diary_id" clearable placeholder="可选">
          <el-option v-for="diary in diaries" :key="diary.id" :label="diary.title" :value="diary.id" />
        </el-select></el-form-item>
        <el-form-item label="地点照片"><input class="file-input" type="file" accept="image/*" multiple @change="chooseFiles" /></el-form-item>
        <p v-if="picked" class="coordinate-tip">已选择坐标：{{ picked.latitude }}, {{ picked.longitude }}</p>
        <PhotoGrid v-if="editing" :photos="editing.photos" />
        <div class="dialog-actions"><el-button @click="dialogVisible = false">取消</el-button><el-button v-if="editing" type="danger" text @click="removePlace(editing)">删除地点</el-button><el-button type="primary" @click="savePlace">保存地点</el-button></div>
      </el-form>
    </el-dialog>
  </section>
</template>
