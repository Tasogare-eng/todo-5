<template>
  <form @submit.prevent="onSubmit" class="space-y-5">
    <div class="space-y-1">
      <label class="block text-sm font-medium">タイトル<span class="text-rose-500">*</span></label>
      <input v-model.trim="form.title" type="text" class="input" required maxlength="100" />
    </div>
    <div class="space-y-1">
      <label class="block text-sm font-medium">説明</label>
      <textarea v-model.trim="form.description" class="input h-28 resize-none" maxlength="1000"></textarea>
    </div>
    <div class="grid grid-cols-2 gap-4">
      <div class="space-y-1">
        <label class="block text-sm font-medium">ステータス</label>
        <select v-model="form.status" class="input">
          <option value="todo">未着手</option>
          <option value="doing">進行中</option>
          <option value="done">完了</option>
        </select>
      </div>
      <div class="space-y-1">
        <label class="block text-sm font-medium">優先度</label>
        <select v-model="form.priority" class="input">
          <option value="high">高</option>
          <option value="medium">中</option>
          <option value="low">低</option>
        </select>
      </div>
    </div>
    <div class="space-y-1">
      <label class="block text-sm font-medium">期限 (日時)</label>
      <input v-model="form.dueDate" type="datetime-local" class="input" />
    </div>
    <div class="flex gap-2 pt-2">
      <button type="submit" class="btn-primary" :disabled="submitting">{{ submitLabel }}</button>
      <button type="button" class="btn-secondary" @click="$emit('cancel')">キャンセル</button>
      <slot name="extra" />
    </div>
  </form>
</template>

<script setup lang="ts">
import { reactive, watchEffect, ref } from 'vue';
import type { TaskInput, Task } from '../types';

interface Props { modelValue?: Task | null; submitLabel?: string }
const props = defineProps<Props>();
const emit = defineEmits(['submit','cancel']);

const empty: TaskInput = { title: '', description: '', status: 'todo', priority: 'medium', dueDate: '' };
const form = reactive<TaskInput>({ ...empty });

watchEffect(() => {
  if (props.modelValue) {
    const { title, description, status, priority, dueDate } = props.modelValue;
    form.title = title;
    form.description = description || '';
    form.status = status;
    form.priority = priority;
    form.dueDate = dueDate ? toLocalInput(dueDate) : '';
  } else {
    Object.assign(form, empty);
  }
});

const submitting = ref(false);

function toLocalInput(iso: string) {
  const d = new Date(iso);
  const tz = new Date(d.getTime() - d.getTimezoneOffset() * 60000);
  return tz.toISOString().slice(0,16);
}

function toIso(local: string) {
  if (!local) return undefined;
  return new Date(local).toISOString();
}

async function onSubmit() {
  submitting.value = true;
  try {
    const payload: TaskInput = {
      title: form.title,
      description: form.description || undefined,
      status: form.status,
      priority: form.priority,
      dueDate: toIso(form.dueDate),
    };
    emit('submit', payload);
  } finally {
    submitting.value = false;
  }
}
</script>

<style scoped>
.input { @apply w-full rounded border border-gray-300 px-3 py-2 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500; }
.btn-primary { @apply bg-indigo-600 text-white text-sm px-4 py-2 rounded hover:bg-indigo-700 disabled:opacity-50; }
.btn-secondary { @apply bg-gray-200 text-gray-800 text-sm px-4 py-2 rounded hover:bg-gray-300; }
</style>
