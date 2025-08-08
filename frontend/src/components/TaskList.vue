<template>
  <div class="space-y-6">
    <div class="flex flex-col md:flex-row md:items-center gap-3">
      <div class="flex flex-wrap items-center gap-3">
        <div class="filter-group">
          <select v-model="statusFilter" @change="fetchTasks()">
            <option value="">すべて</option>
            <option value="todo">未着手</option>
            <option value="doing">進行中</option>
            <option value="done">完了</option>
          </select>
        </div>
        <button class="btn-primary" @click="openCreate">＋ 新規</button>
        <button class="btn-secondary text-xs" @click="fetchTasks">更新</button>
      </div>
    </div>

    <div v-if="loading" class="text-sm text-slate-500 animate-pulse">読み込み中...</div>
    <div v-else-if="error" class="text-sm text-rose-600 bg-rose-50 dark:bg-rose-500/10 border border-rose-200 dark:border-rose-500/30 px-3 py-2 rounded">{{ error }}</div>

    <div v-if="tasks.length === 0 && !loading" class="empty-state">
      <div class="text-4xl">🗒️</div>
      <p>まだタスクがありません。<br/>「＋ 新規」で追加しましょう。</p>
    </div>

    <ul v-else class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      <li v-for="t in tasks" :key="t.id" class="card p-4 flex flex-col gap-3 group">
        <div class="flex items-start justify-between gap-2">
          <div class="min-w-0 flex-1">
            <h2 class="font-semibold text-slate-700 dark:text-slate-100 truncate group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors">{{ t.title }}</h2>
            <p v-if="t.description" class="text-xs text-slate-500 dark:text-slate-400 mt-1 line-clamp-3 whitespace-pre-wrap">{{ t.description }}</p>
          </div>
          <select v-model="t.status" @change="changeStatus(t)" class="input !w-24 !py-1 !px-2 text-[11px]">
            <option value="todo">未着手</option>
            <option value="doing">進行中</option>
            <option value="done">完了</option>
          </select>
        </div>
        <div class="flex flex-wrap gap-2 text-[11px]">
          <span class="badge-status">{{ labelStatus(t.status) }}</span>
          <span :class="priorityBadge(t.priority)">{{ labelPriority(t.priority) }}</span>
          <span v-if="t.dueDate" class="badge bg-slate-100 text-slate-600 dark:bg-slate-700/50 dark:text-slate-300">期限: {{ formatDate(t.dueDate) }}</span>
        </div>
        <div class="flex gap-2 mt-auto pt-1">
          <button class="btn-secondary text-xs" @click="edit(t)">編集</button>
          <button class="btn-danger text-xs" @click="remove(t)">削除</button>
        </div>
      </li>
    </ul>

    <dialog ref="dialogRef" class="p-0 rounded w-full max-w-lg">
      <div class="dialog-panel">
        <div class="dialog-header" v-text="dialogTitle" />
        <div class="dialog-body">
          <TaskForm :model-value="editingTask" :submit-label="dialogSubmitLabel" @submit="save" @cancel="closeDialog" />
        </div>
      </div>
    </dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import { api } from '../api/client';
import type { Task, TaskInput } from '../types';
import TaskForm from './TaskForm.vue';

const tasks = reactive<Task[]>([] as Task[]);
const loading = ref(false);
const error = ref('');
const statusFilter = ref('');
const dialogRef = ref<HTMLDialogElement | null>(null);
const editingTask = ref<Task | null>(null);
const dialogTitle = ref('');
const dialogSubmitLabel = ref('保存');

async function fetchTasks() {
  loading.value = true; error.value='';
  try {
    const data: Task[] = await api.listTasks(statusFilter.value || undefined);
    tasks.splice(0, tasks.length, ...data);
  } catch (e:any) {
    const msg = e?.message || '';
    if (msg.includes('404')) {
      // タスクゼロとして扱い、エラーは表示しない
      tasks.splice(0, tasks.length);
      error.value = '';
    } else {
      error.value = msg || '読み込み失敗';
    }
  } finally {
    loading.value = false;
  }
}

function openCreate() {
  editingTask.value = null;
  dialogTitle.value = 'タスク作成';
  dialogSubmitLabel.value = '作成';
  dialogRef.value?.showModal();
}

function edit(t: Task) {
  editingTask.value = { ...t };
  dialogTitle.value = 'タスク編集';
  dialogSubmitLabel.value = '更新';
  dialogRef.value?.showModal();
}

function closeDialog() {
  dialogRef.value?.close();
}

async function save(input: TaskInput) {
  try {
    if (editingTask.value) {
      const updated = await api.updateTask(editingTask.value.id, input);
      const idx = tasks.findIndex(x => x.id === editingTask.value?.id);
      if (idx >= 0) tasks[idx] = updated as Task;
    } else {
      const created = await api.createTask(input);
      tasks.unshift(created as Task);
    }
    closeDialog();
  } catch (e:any) {
    alert(e.message);
  }
}

async function changeStatus(t: Task) {
  try {
    const updated = await api.patchTask(t.id, { status: t.status });
    Object.assign(t, updated);
  } catch (e:any) {
    alert(e.message);
  }
}

async function remove(t: Task) {
  if (!confirm('削除しますか？')) return;
  try {
    await api.deleteTask(t.id);
    const idx = tasks.findIndex(x => x.id === t.id);
    if (idx >= 0) tasks.splice(idx,1);
  } catch (e:any) {
    alert(e.message);
  }
}

function formatDate(iso: string) {
  const d = new Date(iso);
  return new Intl.DateTimeFormat('ja-JP', { dateStyle: 'short', timeStyle: 'short' }).format(d);
}

function labelStatus(s: Task['status']) {
  switch(s){
    case 'todo': return '未着手';
    case 'doing': return '進行中';
    case 'done': return '完了';
  }
}
function labelPriority(p: Task['priority']) {
  switch(p){
    case 'high': return '高';
    case 'medium': return '中';
    case 'low': return '低';
  }
}
function priorityBadge(p: Task['priority']) {
  if (p==='high') return 'badge-priority-high';
  if (p==='medium') return 'badge-priority-medium';
  return 'badge-priority-low';
}

fetchTasks();
</script>

<style scoped>
.input { @apply w-full rounded border border-gray-300 px-2 py-1 text-xs bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500; }
.btn-primary { @apply bg-indigo-600 text-white text-xs px-3 py-1.5 rounded hover:bg-indigo-700 disabled:opacity-50; }
.btn-secondary { @apply bg-gray-200 text-gray-800 text-xs px-3 py-1.5 rounded hover:bg-gray-300; }
.btn-danger { @apply bg-red-500 text-white text-xs px-3 py-1.5 rounded hover:bg-red-600; }
</style>
