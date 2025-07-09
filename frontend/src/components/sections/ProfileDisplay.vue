<template>
  <AppCard class="mb-6" :class="{ 'animate-fade-in': isVisible }">
    <div class="flex items-start gap-4">
      <div class="flex-shrink-0 p-3 bg-tribal-lime/20 rounded-lg">
        <AppIcon name="profile" :size="24" color="#B9FBC0" />
      </div>
      <div class="flex-1">
        <h3 class="text-xl font-semibold text-soft-white mb-2">
          Cultural Profile: {{ profile.identity }}
        </h3>
        <p class="text-gray-300 leading-relaxed mb-4">
          {{ profile.description }}
        </p>
        <div class="space-y-3">
          <div>
            <h4 class="text-sm font-medium text-gray-400 mb-2">Music Preferences</h4>
            <div class="flex flex-wrap gap-2">
              <AppChip
                v-for="genre in profile.music"
                :key="genre"
                variant="accent"
                size="sm"
              >
                {{ genre }}
              </AppChip>
            </div>
          </div>
          <div>
            <h4 class="text-sm font-medium text-gray-400 mb-2">Style Elements</h4>
            <div class="flex flex-wrap gap-2">
              <AppChip
                v-for="style in profile.style"
                :key="style"
                variant="secondary"
                size="sm"
              >
                {{ style }}
              </AppChip>
            </div>
          </div>
        </div>
      </div>
    </div>
  </AppCard>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import AppCard from '@/components/ui/AppCard.vue';
import AppIcon from '@/components/ui/AppIcon.vue';
import AppChip from '@/components/ui/AppChip.vue';
import type { CulturalProfile } from '@/types';

interface Props {
  profile: CulturalProfile;
  delay?: number;
}

const props = withDefaults(defineProps<Props>(), {
  delay: 0
});

const isVisible = ref(false);

onMounted(() => {
  setTimeout(() => {
    isVisible.value = true;
  }, props.delay);
});
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