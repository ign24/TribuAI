<template>
  <div class="card-glass rounded-2xl p-6">
    <div class="flex items-start gap-4">
      <div class="w-12 h-12 rounded-xl bg-gradient-neon flex items-center justify-center flex-shrink-0 shadow-md shadow-tribal-lime/20">
        <AppIcon name="profile" :size="20" color="white" />
      </div>
      <div class="flex-1 min-w-0">
        <h3 class="text-lg font-bold text-soft-white mb-2">
          {{ profile.identity }}
        </h3>
        <p class="text-sm text-gray-300 leading-relaxed mb-4">
          {{ profile.description }}
        </p>
        
        <div class="space-y-4">
          <div>
            <h4 class="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-2">Music Preferences</h4>
            <div class="flex flex-wrap gap-2">
              <span
                v-for="genre in profile.music"
                :key="genre"
                class="chip chip-success"
              >
                {{ genre }}
              </span>
            </div>
          </div>
          
          <div>
            <h4 class="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-2">Style Elements</h4>
            <div class="flex flex-wrap gap-2">
              <span
                v-for="style in profile.style"
                :key="style"
                class="chip chip-primary"
              >
                {{ style }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import AppIcon from '@/components/ui/AppIcon.vue';
import type { CulturalProfile } from '@/types';

interface Props {
  profile: CulturalProfile;
}

defineProps<Props>();
</script>