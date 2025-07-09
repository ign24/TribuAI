<template>
  <div class="min-h-screen bg-obsidian text-soft-white">
    <!-- Background Effects -->
    <div class="fixed inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-1/4 left-1/4 w-64 h-64 bg-rust-red/10 rounded-full blur-3xl"></div>
      <div class="absolute bottom-1/4 right-1/4 w-96 h-96 bg-slate-blue/10 rounded-full blur-3xl"></div>
      <div class="absolute top-3/4 left-1/2 w-80 h-80 bg-tribal-lime/5 rounded-full blur-3xl"></div>
    </div>
    
    <!-- Content -->
    <div class="relative z-10">
      <AppHeader v-if="showHeader" />
      <main class="pb-8">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import AppHeader from './AppHeader.vue';

interface Props {
  showHeader?: boolean;
}

withDefaults(defineProps<Props>(), {
  showHeader: true
});
</script>