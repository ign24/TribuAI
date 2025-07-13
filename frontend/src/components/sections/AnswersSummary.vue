<template>
  <AppCard class="mb-8" :class="{ 'animate-fade-in': isVisible }">
    <div class="flex items-start gap-4">
      <div class="flex-shrink-0 p-3 bg-slate-blue/20 rounded-lg">
        <AppIcon name="summary" :size="24" color="#3A86FF" />
      </div>
      <div class="flex-1">
        <h3 class="text-xl font-semibold text-soft-white mb-4">
          Summary of Your Cultural Identity
        </h3>
        <div class="space-y-4">
          <div class="p-4 bg-gray-800/30 rounded-lg border border-gray-700/50">
            <h4 class="text-sm font-medium text-gray-400 mb-2">Your Input</h4>
            <p class="text-gray-300 leading-relaxed">{{ userInput }}</p>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="p-4 bg-gray-800/30 rounded-lg border border-gray-700/50">
              <h4 class="text-sm font-medium text-gray-400 mb-3">Key Themes</h4>
              <div class="flex flex-wrap gap-2">
                <AppChip
                  v-for="theme in keyThemes"
                  :key="theme"
                  variant="accent"
                  size="sm"
                >
                  {{ theme }}
                </AppChip>
              </div>
            </div>
            
            <div class="p-4 bg-gray-800/30 rounded-lg border border-gray-700/50">
              <h4 class="text-sm font-medium text-gray-400 mb-3">Cultural Markers</h4>
              <div class="space-y-2">
                <div class="flex items-center gap-2 text-sm text-gray-300">
                  <div class="w-2 h-2 bg-tribal-lime rounded-full"></div>
                  <span>{{ culturalMarkers.creative }}</span>
                </div>
                <div class="flex items-center gap-2 text-sm text-gray-300">
                  <div class="w-2 h-2 bg-rust-red rounded-full"></div>
                  <span>{{ culturalMarkers.values }}</span>
                </div>
                <div class="flex items-center gap-2 text-sm text-gray-300">
                  <div class="w-2 h-2 bg-slate-blue rounded-full"></div>
                  <span>{{ culturalMarkers.aesthetics }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </AppCard>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import AppCard from '@/components/ui/AppCard.vue';
import AppIcon from '@/components/ui/AppIcon.vue';
import AppChip from '@/components/ui/AppChip.vue';

interface Props {
  userInput: string;
  culturalProfile?: any;
  delay?: number;
}

const props = withDefaults(defineProps<Props>(), {
  delay: 800
});

const isVisible = ref(false);

// Extract key themes from cultural profile
const keyThemes = computed(() => {
  if (!props.culturalProfile) {
    // Fallback to input analysis
    const input = props.userInput.toLowerCase();
    const possibleThemes = [
      'music', 'art', 'fashion', 'design', 'sustainability', 
      'creativity', 'minimalism', 'urban', 'authentic', 'modern'
    ];
    
    return possibleThemes.filter(theme => 
      input.includes(theme) || input.includes(theme.slice(0, -1))
    ).slice(0, 6);
  }
  
  // Use real data from cultural profile
  const themes = [];
  if (props.culturalProfile.music) {
    themes.push(...props.culturalProfile.music.slice(0, 2));
  }
  if (props.culturalProfile.style) {
    themes.push(...props.culturalProfile.style.slice(0, 2));
  }
  if (props.culturalProfile.values) {
    themes.push(...props.culturalProfile.values.slice(0, 2));
  }
  
  return themes.slice(0, 6);
});

// Cultural markers based on profile
const culturalMarkers = computed(() => {
  if (!props.culturalProfile) {
    return {
      creative: 'Creative Expression',
      values: 'Authentic Values', 
      aesthetics: 'Contemporary Aesthetics'
    };
  }
  
  return {
    creative: props.culturalProfile.identity?.includes('Creative') ? 'Creative Expression' : 'Artistic Sensibility',
    values: props.culturalProfile.values?.[0] || 'Authentic Values',
    aesthetics: props.culturalProfile.style?.[0] || 'Contemporary Aesthetics'
  };
});

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