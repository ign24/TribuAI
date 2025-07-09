<template>
  <AppCard class="mb-6" :class="{ 'animate-fade-in': isVisible }">
    <div class="flex items-start gap-4">
      <div class="flex-shrink-0 p-3 bg-tribal-lime/20 rounded-lg">
        <AppIcon name="match" :size="24" color="#B9FBC0" />
      </div>
      <div class="flex-1">
        <h3 class="text-xl font-semibold text-soft-white mb-4">
          Cultural Compatibility
        </h3>
        <div class="p-4 bg-gradient-to-r from-tribal-lime/10 to-slate-blue/10 rounded-lg border border-tribal-lime/30">
          <div class="flex items-center justify-between mb-3">
            <div>
              <p class="text-lg font-semibold text-soft-white">
                Audience cluster: <span class="text-tribal-lime">{{ matching.audience_cluster }}</span>
              </p>
              <div v-if="matching.shared_interests && matching.shared_interests.length" class="text-xs text-gray-400 mt-1">
                Shared interests: {{ matching.shared_interests.join(', ') }}
              </div>
            </div>
            <div class="text-right">
              <div class="text-3xl font-bold text-tribal-lime mb-1">
                {{ matching.affinity_percentage }}%
              </div>
              <div class="text-xs text-gray-400">affinity</div>
            </div>
          </div>
          <!-- Progress Bar -->
          <div class="w-full bg-gray-700 rounded-full h-2 mb-2">
            <div
              class="bg-gradient-to-r from-tribal-lime to-slate-blue h-2 rounded-full transition-all duration-1000 ease-out"
              :style="{ width: animateProgress ? `${matching.affinity_percentage}%` : '0%' }"
            ></div>
          </div>
          <p class="text-xs text-gray-400 text-center">
            High affinity suggests shared values and aesthetic preferences
          </p>
        </div>
      </div>
    </div>
  </AppCard>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import AppCard from '@/components/ui/AppCard.vue';
import AppIcon from '@/components/ui/AppIcon.vue';
import type { Matching } from '@/types';

interface Props {
  matching: Matching;
  delay?: number;
}

const props = withDefaults(defineProps<Props>(), {
  delay: 600
});

const isVisible = ref(false);
const animateProgress = ref(false);

// Eliminado: progressWidth, ya no se usa match_percentage

onMounted(() => {
  setTimeout(() => {
    isVisible.value = true;
    setTimeout(() => {
      animateProgress.value = true;
    }, 300);
  }, props.delay);
});

// Eliminar isObject y lógica de nombres/edad/location
</script>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.6s ease-out forwards;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>