<template>
  <AppCard class="mb-8 animate-fade-in">
    <div class="flex items-start gap-4">
      <div class="flex-shrink-0 p-3 bg-gradient-accent rounded-lg">
        <AppIcon name="match" :size="24" color="#3A86FF" />
      </div>
      <div class="flex-1">
        <h3 class="text-xl font-semibold text-soft-white mb-4">
          Personalized Recommendations
        </h3>
        <div v-if="hasAnyRecommendations" class="space-y-8">
          <div v-for="(items, type) in groupedRecommendations" :key="type">
            <h4 class="text-lg font-bold text-tribal-lime mb-2 capitalize">{{ formatType(String(type)) }}</h4>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div v-for="item in items" :key="String(item.entity_id || item.name)" class="p-4 bg-gray-800/30 rounded-lg border border-gray-700/50 flex gap-4">
                <div class="w-16 h-16 rounded-lg bg-gradient-neon flex items-center justify-center flex-shrink-0 overflow-hidden">
                  <img v-if="item.image && item.image.url" :src="item.image.url" :alt="item.name" class="w-full h-full object-cover" />
                  <AppIcon v-else name="match" :size="24" color="#3A86FF" />
                </div>
                <div class="flex-1 min-w-0">
                  <h5 class="font-semibold text-soft-white text-base truncate">{{ item.name }}</h5>
                  <p v-if="item.description" class="text-xs text-gray-400 line-clamp-2 mb-1">{{ item.description }}</p>
                  <div v-if="item.tags && item.tags.length > 0" class="flex flex-wrap gap-1 mt-1">
                    <span v-for="tag in item.tags.slice(0, 3)" :key="String(tag.name)" class="text-xs px-2 py-1 rounded-full bg-slate-blue/20 text-gray-300">
                      {{ tag.name }}
                    </span>
                  </div>
                  <a v-if="item.website" :href="item.website" target="_blank" class="text-xs text-tribal-lime underline mt-1 inline-block">Visit website</a>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="text-gray-400 text-sm py-8 text-center">
          No recommendations found for your profile. Try adjusting your preferences!
        </div>
      </div>
    </div>
  </AppCard>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import AppCard from '@/components/ui/AppCard.vue';
import AppIcon from '@/components/ui/AppIcon.vue';

interface RecommendationItem {
  entity_id?: string;
  name: string;
  description?: string;
  image?: { url: string };
  tags?: Array<{ name: string }>;
  website?: string;
  [key: string]: any;
}

interface Props {
  recommendations: Record<string, RecommendationItem[]>;
}

const props = defineProps<Props>();

const groupedRecommendations = computed(() => {
  // Group by type, only show non-empty arrays
  return Object.fromEntries(
    Object.entries(props.recommendations || {})
      .filter(([_, arr]) => Array.isArray(arr) && arr.length > 0)
  );
});

const hasAnyRecommendations = computed(() => {
  return Object.keys(groupedRecommendations.value).length > 0;
});

function formatType(type: string) {
  // Capitalize and make more readable
  switch (type) {
    case 'brands': return 'Brands';
    case 'places': return 'Places';
    case 'books': return 'Books';
    case 'albums': return 'Albums';
    case 'artists': return 'Artists';
    default: return type.charAt(0).toUpperCase() + type.slice(1);
  }
}
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
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style> 