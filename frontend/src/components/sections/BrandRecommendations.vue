<template>
  <AppCard class="mb-6" :class="{ 'animate-fade-in': isVisible }">
    <div class="flex items-start gap-4">
      <div class="flex-shrink-0 p-3 bg-slate-blue/20 rounded-lg">
        <AppIcon name="brands" :size="24" color="#3A86FF" />
      </div>
      <div class="flex-1">
        <h3 class="text-xl font-semibold text-soft-white mb-4">
          Brand Recommendations
        </h3>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <div
            v-for="(brand, index) in normalizedBrands"
            :key="brand.entity_id"
            class="brand-card"
            :style="{ animationDelay: `${index * 100}ms` }"
          >
            <div class="p-4 bg-gray-800/50 rounded-lg border border-gray-700 hover:border-slate-blue/50 transition-all duration-200 hover:bg-gray-700/50">
              <!-- Brand Image or Default Icon -->
              <div class="mb-3 w-full h-24 flex items-center justify-center bg-gray-900/40 rounded-lg">
                <img 
                  v-if="brand.image && !brand._imageError" 
                  :src="brand.image" 
                  :alt="brand.name"
                  class="w-full h-24 object-cover rounded-lg"
                  @error="() => brand._imageError = true"
                />
                <AppIcon v-else name="brands" :size="40" color="#3A86FF" />
              </div>
              
              <!-- Brand Name -->
              <h4 class="text-lg font-semibold text-soft-white mb-2">{{ brand.name }}</h4>
              
              <!-- Brand Description -->
              <p v-if="brand.description" class="text-sm text-gray-300 mb-3 line-clamp-2">
                {{ brand.description }}
              </p>
              
              <!-- Brand Tags -->
              <div v-if="brand.tags && brand.tags.length > 0" class="flex flex-wrap gap-1">
                <span
                  v-for="tag in brand.tags.slice(0, 3)"
                  :key="tag"
                  class="px-2 py-1 text-xs bg-slate-blue/20 text-slate-blue rounded-full"
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
  brands: (EnrichedEntity | string)[];
  delay?: number;
}

const props = withDefaults(defineProps<Props>(), {
  delay: 200
});

const isVisible = ref(false);

// Convert strings to EnrichedEntity for backward compatibility
const normalizedBrands = computed(() => {
  return props.brands.map(brand => {
    if (typeof brand === 'string') {
      return {
        name: brand,
        entity_id: `legacy_${brand.toLowerCase().replace(/\s+/g, '_')}`,
        description: '',
        image: '',
        tags: [],
        _imageError: false
      } as EnrichedEntity & { _imageError: boolean };
    }
    return { ...brand, _imageError: false } as EnrichedEntity & { _imageError: boolean };
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

.animate-fade-in .brand-card {
  animation: slideUp 0.4s ease-out forwards;
  opacity: 0;
  transform: translateY(20px);
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