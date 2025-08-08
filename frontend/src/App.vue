<template>
  <div :class="['app-shell', dark ? 'dark' : '']">
    <header class="app-header">
      <div class="app-header-inner">
        <div class="flex items-center gap-3">
          <span class="brand">TODO アプリ</span>
          <span class="hidden sm:inline text-xs text-slate-500 dark:text-slate-400">シンプルなタスク管理</span>
        </div>
        <div class="flex items-center gap-2">
          <button class="btn-ghost" @click="toggleDark" aria-label="テーマ切替">
            <span v-if="!dark">🌙</span>
            <span v-else>☀️</span>
          </button>
          <a href="https://fastapi.tiangolo.com/" target="_blank" class="btn-secondary text-xs">API Docs</a>
        </div>
      </div>
    </header>

    <main class="flex-1 w-full max-w-5xl mx-auto px-4 py-8">
      <TaskList />
    </main>

    <footer class="text-xs text-center text-slate-500 dark:text-slate-500 py-6">
      © 2025 / Built with FastAPI + Vue 3 + Tailwind
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, watchEffect } from 'vue';
import TaskList from './components/TaskList.vue';

const dark = ref(false);

function toggleDark() { dark.value = !dark.value; }

// Persist (localStorage)
const KEY = 'todoapp:dark';
if (localStorage.getItem(KEY) === '1') dark.value = true;
watchEffect(() => { localStorage.setItem(KEY, dark.value ? '1' : '0'); });
</script>

<style scoped>
</style>
