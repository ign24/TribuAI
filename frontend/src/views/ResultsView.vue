<template>
  <AppLayout>
    <div class="max-w-4xl mx-auto px-6 py-8">
      <div v-if="api.hasData.value && api.data.value">
        <!-- Debug Section (temporary) -->
        <div class="mb-8 p-4 bg-gray-800 rounded-lg">
          <h3 class="text-lg font-semibold text-white mb-4">Debug Info</h3>
          <div class="text-sm text-gray-300 space-y-2">
            <div><strong>Cultural Profile:</strong> {{ JSON.stringify(api.data.value.cultural_profile, null, 2) }}</div>
            <div><strong>Recommendations:</strong> {{ JSON.stringify(api.data.value.recommendations, null, 2) }}</div>
            <div><strong>Matching:</strong> {{ JSON.stringify(api.data.value.matching, null, 2) }}</div>
          </div>
        </div>
        
        <!-- Profile Display -->
        <ProfileDisplay 
          :profile="api.data.value.cultural_profile"
          :delay="0"
        />
        
        <!-- Brand Recommendations -->
        <BrandRecommendations 
          :brands="api.data.value.recommendations.brands"
          :delay="200"
        />
        
        <!-- Geographic Affinities -->
        <GeographicAffinities 
          :places="api.data.value.recommendations.places"
          :delay="400"
        />
        
        <!-- Cultural Compatibility -->
        <CulturalCompatibility 
          v-if="api.data.value.matching"
          :matching="api.data.value.matching"
          :delay="600"
        />
        
        <!-- Answers Summary -->
        <AnswersSummary 
          v-if="userInput"
          :user-input="userInput"
          :delay="800"
        />
        
        <!-- Action Buttons -->
        <div class="flex flex-col sm:flex-row gap-4 justify-center items-center">
          <AppButton
            variant="primary"
            size="lg"
            @click="discoverAnother"
          >
            <AppIcon name="refresh" :size="20" class="mr-2" />
            Discover Another Tribe
          </AppButton>
          
          <AppButton
            variant="secondary"
            size="lg"
            @click="shareResults"
          >
            Share Your Profile
          </AppButton>
        </div>
      </div>
      
      <!-- Loading State -->
      <div v-else-if="api.loading.value" class="text-center py-16">
        <div class="loading-pulse mb-4"></div>
        <p class="text-xl text-gray-300">Analyzing your cultural identity...</p>
        <p class="text-sm text-gray-400 mt-2">This may take a moment</p>
      </div>
      
      <!-- Error State -->
      <div v-else-if="api.error.value" class="text-center py-16">
        <AppCard class="max-w-md mx-auto">
          <p class="text-red-400 mb-4">Something went wrong while analyzing your profile.</p>
          <p class="text-sm text-gray-400 mb-4">{{ api.errorMessage.value }}</p>
          <AppButton variant="secondary" @click="$router.push('/')">
            Try Again
          </AppButton>
        </AppCard>
      </div>
      
      <!-- No Data State -->
      <div v-else class="text-center py-16">
        <AppCard class="max-w-md mx-auto">
          <p class="text-gray-300 mb-4">No cultural profile found. Let's start your journey.</p>
          <AppButton variant="primary" @click="$router.push('/')">
            Discover Your Tribe
          </AppButton>
        </AppCard>
      </div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import AppLayout from '@/components/layout/AppLayout.vue';
import AppButton from '@/components/ui/AppButton.vue';
import AppCard from '@/components/ui/AppCard.vue';
import AppIcon from '@/components/ui/AppIcon.vue';
import ProfileDisplay from '@/components/sections/ProfileDisplay.vue';
import BrandRecommendations from '@/components/sections/BrandRecommendations.vue';
import GeographicAffinities from '@/components/sections/GeographicAffinities.vue';
import CulturalCompatibility from '@/components/sections/CulturalCompatibility.vue';
import AnswersSummary from '@/components/sections/AnswersSummary.vue';
import { useApi } from '@/composables/useApi';

const router = useRouter();
const api = useApi();
const userInput = ref('');

onMounted(() => {
  // Get the stored user input
  const storedInput = sessionStorage.getItem('tribuai_user_input');
  if (storedInput) {
    userInput.value = storedInput;
  }
  
  // If no data, redirect to home
  if (!api.hasData.value) {
    router.push('/');
  }
});

watch(
  () => api.data.value,
  (val) => {
    if (val) {
      console.log('[TribuAI] ResultsView: api.data.value', val);
      console.log('[TribuAI] ProfileDisplay props:', val.cultural_profile);
      console.log('[TribuAI] BrandRecommendations props:', val.recommendations.brands);
      console.log('[TribuAI] GeographicAffinities props:', val.recommendations.places);
      console.log('[TribuAI] CulturalCompatibility props:', val.matching);
    }
  },
  { immediate: true }
);

const discoverAnother = () => {
  api.reset();
  sessionStorage.removeItem('tribuai_user_input');
  router.push('/');
};

const shareResults = () => {
  if (navigator.share && api.data.value) {
    navigator.share({
      title: 'My Cultural Profile - TribuAI',
      text: `I'm a ${api.data.value.cultural_profile.identity}! Discover your cultural identity with TribuAI.`,
      url: window.location.origin
    });
  } else {
    // Fallback: copy to clipboard
    const text = `I'm a ${api.data.value?.cultural_profile.identity}! Discover your cultural identity at ${window.location.origin}`;
    navigator.clipboard.writeText(text);
    // You could show a toast notification here
  }
};
</script>

<style scoped>
.loading-pulse {
  @apply w-16 h-16 mx-auto rounded-full;
  background: linear-gradient(45deg, #B9FBC0, #3A86FF, #D95D39);
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.7;
  }
}
</style>