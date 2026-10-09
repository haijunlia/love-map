<script setup>
import { reactive, ref } from "vue";
import { ElMessage } from "element-plus";
import { today, moodMeta } from "../composables/useLove";

const props = defineProps({
  diary: { type: Object, default: null }
});
const emit = defineEmits(["submit", "cancel"]);
const formRef = ref();
const files = ref([]);
const form = reactive({
  diary_date: props.diary?.diary_date || today(),
  title: props.diary?.title || "",
  content: props.diary?.content || "",
  mood: props.diary?.mood || "happy"
});
const rules = {
  diary_date: [{ required: true, message: "请选择日期", trigger: "change" }],
  title: [{ required: true, message: "请填写标题", trigger: "blur" }],
  content: [{ required: true, message: "请填写内容", trigger: "blur" }]
};

function chooseFiles(event) {
  files.value = Array.from(event.target.files || []);
}

async function submit() {
  const valid = await formRef.value.validate().catch(() => false);
  if (!valid) return;
  if (files.value.some((file) => file.size > 10 * 1024 * 1024)) {
    ElMessage.warning("单张照片不能超过 10 MB");
    return;
  }
  emit("submit", { data: { ...form }, files: files.value });
}
</script>

<template>
  <el-form ref="formRef" :model="form" :rules="rules" label-position="top" class="diary-form">
    <div class="form-two-columns">
      <el-form-item label="日期" prop="diary_date">
        <el-date-picker v-model="form.diary_date" type="date" value-format="YYYY-MM-DD" placeholder="选择日期" />
      </el-form-item>
      <el-form-item label="心情" prop="mood">
        <el-select v-model="form.mood" placeholder="选择心情">
          <el-option v-for="(meta, key) in moodMeta" :key="key" :label="meta.icon + ' ' + meta.label" :value="key" />
        </el-select>
      </el-form-item>
    </div>
    <el-form-item label="标题" prop="title">
      <el-input v-model="form.title" maxlength="120" show-word-limit placeholder="例如：第一次一起看海" />
    </el-form-item>
    <el-form-item label="内容" prop="content">
      <el-input v-model="form.content" type="textarea" :rows="6" maxlength="10000" show-word-limit placeholder="写下今天想收藏的片段..." />
    </el-form-item>
    <el-form-item label="照片">
      <input class="file-input" type="file" accept="image/*" multiple @change="chooseFiles" />
      <small class="form-tip">{{ files.length ? "已选择 " + files.length + " 张照片" : "支持 JPG、PNG、GIF、WebP，单张不超过 10 MB" }}</small>
    </el-form-item>
    <div class="dialog-actions">
      <el-button @click="emit('cancel')">取消</el-button>
      <el-button type="primary" @click="submit">保存日记</el-button>
    </div>
  </el-form>
</template>
