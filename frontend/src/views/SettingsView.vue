<script setup>
import { reactive, watch } from "vue";
import { ElMessage } from "element-plus";
import { api } from "../services/api";

const props = defineProps({ couple: { type: Object, default: null } });
const emit = defineEmits(["saved"]);
const form = reactive({ nickname_a: "", nickname_b: "", anniversary: "" });

watch(() => props.couple, (value) => {
  form.nickname_a = value?.nickname_a || "";
  form.nickname_b = value?.nickname_b || "";
  form.anniversary = value?.anniversary || "";
}, { immediate: true });

async function save() {
  if (!form.nickname_a || !form.nickname_b || !form.anniversary) {
    ElMessage.warning("请填写完整信息");
    return;
  }
  try {
    const saved = await api.saveCouple(form);
    ElMessage.success("情侣信息已保存");
    emit("saved", saved);
  } catch (error) {
    ElMessage.error(error.message);
  }
}
</script>

<template>
  <section class="page-section settings-page">
    <div class="page-title-row"><div><span class="eyebrow">OUR STORY</span><h1>设置我们的空间</h1><p>这些信息只保存在你自己的本地数据库中。</p></div></div>
    <div class="settings-layout">
      <el-card class="settings-card" shadow="never">
        <h2>关于我们</h2>
        <el-form label-position="top">
          <el-form-item label="昵称 A"><el-input v-model="form.nickname_a" placeholder="例如：小明" /></el-form-item>
          <el-form-item label="昵称 B"><el-input v-model="form.nickname_b" placeholder="例如：小红" /></el-form-item>
          <el-form-item label="在一起的纪念日"><el-date-picker v-model="form.anniversary" type="date" value-format="YYYY-MM-DD" /></el-form-item>
          <el-button type="primary" round @click="save">保存设置</el-button>
        </el-form>
      </el-card>
      <div class="soft-note"><span class="soft-note-icon">✿</span><h2>一个只属于你们的角落</h2><p>照片会保存到 backend/uploads，数据会保存到 SQLite。项目默认只在本机运行，适合先记录和学习。</p></div>
    </div>
  </section>
</template>
