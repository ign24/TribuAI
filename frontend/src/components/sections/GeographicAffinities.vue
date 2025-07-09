<template>
  <AppCard class="mb-6" :class="{ 'animate-fade-in': isVisible }">
    <div class="flex items-start gap-4">
      <div class="flex-shrink-0 p-3 bg-rust-red/20 rounded-lg">
        <AppIcon name="globe" :size="24" color="#D95D39" />
      </div>
      <div class="flex-1">
        <h3 class="text-xl font-semibold text-soft-white mb-4">
          Geographic Affinities
        </h3>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <div
            v-for="(place, index) in normalizedPlaces"
            :key="place.entity_id"
            class="place-card"
            :style="{ animationDelay: `${index * 150}ms` }"
          >
            <div class="p-4 bg-gray-800/30 rounded-lg border border-gray-700/50 hover:border-rust-red/50 transition-all duration-200">
              <!-- Place Image or Default Icon -->
              <div class="mb-3 w-full h-24 flex items-center justify-center bg-gray-900/40 rounded-lg">
                <img 
                  v-if="place.image && !place._imageError" 
                  :src="place.image" 
                  :alt="place.name"
                  class="w-full h-24 object-cover rounded-lg"
                  @error="() => place._imageError = true"
                />
                <AppIcon v-else name="globe" :size="40" color="#D95D39" />
              </div>
              
              <!-- Place Name -->
              <div class="flex items-center gap-2 mb-2">
              <AppIcon name="arrow-right" :size="16" color="#D95D39" />
                <h4 class="text-lg font-semibold text-soft-white">{{ place.name }}</h4>
              </div>
              
              <!-- Place Description -->
              <p v-if="place.description" class="text-sm text-gray-300 mb-3 line-clamp-2">
                {{ place.description }}
              </p>
              
              <!-- Place Tags -->
              <div v-if="place.tags && place.tags.length > 0" class="flex flex-wrap gap-1">
                <span
                  v-for="tag in place.tags.slice(0, 3)"
                  :key="tag"
                  class="px-2 py-1 text-xs bg-rust-red/20 text-rust-red rounded-full"
                >
                  {{ tag }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </AppCard>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import AppCard from '@/components/ui/AppCard.vue';
import AppIcon from '@/components/ui/AppIcon.vue';
import type { EnrichedEntity } from '@/types';

interface Props {
  places: (EnrichedEntity | string)[];
  delay?: number;
}

const props = withDefaults(defineProps<Props>(), {
  delay: 400
});

const isVisible = ref(false);

// Convert strings to EnrichedEntity for backward compatibility
const normalizedPlaces = computed(() => {
  return props.places.map(place => {
    if (typeof place === 'string') {
      return {
        name: place,
        entity_id: `legacy_${place.toLowerCase().replace(/\s+/g, '_')}`,
        description: '',
        image: '',
        tags: [],
        _imageError: false
      } as EnrichedEntity & { _imageError: boolean };
    }
    return { ...place, _imageError: false } as EnrichedEntity & { _imageError: boolean };
  });
});

onMounted(() => {
  setTimeout(() => {
    isVisible.value = true;
  }, props.delay);
});

const handleImageError = (event: Event) => {
  const img = event.target as HTMLImageElement;
  img.style.display = 'none';
};
</script>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.6s ease-out forwards;
}

.animate-fade-in .place-card {
  animation: slideUp 0.4s ease-out forwards;
  opacity: 0;
  transform: translateY(15px);
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

@keyframes slideUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>