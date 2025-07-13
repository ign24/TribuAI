<template>
  <div class="card-glass rounded-2xl p-6">
    <div class="flex items-center gap-3 mb-4">
      <div class="w-10 h-10 rounded-lg bg-gradient-neon flex items-center justify-center shadow-md shadow-tribal-lime/20">
        <AppIcon name="match" :size="16" color="white" />
      </div>
      <div>
        <h3 class="text-base font-bold text-soft-white">Cultural Match</h3>
        <p class="text-xs text-gray-400">Your tribe compatibility</p>
      </div>
    </div>
    
    <div class="p-4 rounded-xl bg-gradient-to-r from-tribal-lime/10 to-slate-blue/10 border border-tribal-lime/30">
          <div class="flex items-center justify-between mb-3">
            <div>
          <p class="font-semibold text-soft-white text-sm">
            Cluster: <span class="text-tribal-lime">{{ matching.audience_cluster }}</span>
              </p>
          <p class="text-xs text-gray-400">Cultural alignment</p>
            </div>
            <div class="text-right">
          <div class="text-2xl font-bold text-tribal-lime">
            {{ matching.affinity_percentage }}%
              </div>
          <div class="text-xs text-gray-400">affinity</div>
            </div>
          </div>
          
          <!-- Progress Bar -->
      <div class="w-full bg-gray-700/50 rounded-full h-2 mb-3">
            <div
              class="bg-gradient-to-r from-tribal-lime to-slate-blue h-2 rounded-full transition-all duration-1000 ease-out"
              :style="{ width: progressWidth }"
            ></div>
          </div>
          
      <!-- Shared Interests -->
      <div v-if="matching.shared_interests && matching.shared_interests.length > 0" class="mb-3">
        <p class="text-xs text-gray-400 mb-2">Shared interests:</p>
        <div class="flex flex-wrap gap-1">
          <span 
            v-for="interest in matching.shared_interests.slice(0, 4)" 
            :key="interest"
            class="text-xs px-2 py-1 rounded-full bg-tribal-lime/20 text-tribal-lime"
          >
            {{ interest }}
          </span>
        </div>
      </div>
      
      <p class="text-xs text-gray-400 text-center">
        High affinity suggests shared cultural values
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import AppIcon from '@/components/ui/AppIcon.vue';
import type { Matching } from '@/types';

interface Props {
  matching: Matching;
}

const props = defineProps<Props>();

const animateProgress = ref(false);

const progressWidth = computed(() => 
  animateProgress.value ? `${props.matching.affinity_percentage}%` : '0%'
);

onMounted(() => {
    setTimeout(() => {
      animateProgress.value = true;
    }, 300);
});
</script>