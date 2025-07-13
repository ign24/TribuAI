<template>
  <AppLayout>
    <div class="container mx-auto h-[calc(100vh-64px)]">
      <!-- DEBUG BLOCK -->
      <div class="mb-6 p-4 rounded-lg bg-gray-900/80 border border-tribal-lime/40 text-xs text-tribal-lime">
        <strong>DEBUG:</strong><br>
        <div>recommendations: <pre style="white-space: pre-wrap; word-break: break-all;">{{ JSON.stringify(recommendations, null, 2) }}</pre></div>
        <div>matching: <pre style="white-space: pre-wrap; word-break: break-all;">{{ JSON.stringify(matching, null, 2) }}</pre></div>
      </div>
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 h-full p-6">
        
        <!-- Chat Section -->
        <div class="lg:col-span-2 flex flex-col">
          <div class="card-glass rounded-2xl flex flex-col h-full overflow-hidden">
            
            <!-- Chat Header -->
            <div class="p-6 border-b border-default">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-2">
                  <div class="status-typing" v-if="isLoading">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                  </div>
                  <span class="text-xs text-gray-400" v-else>Ready to chat</span>
                </div>
                <div v-if="error" class="text-xs text-red-400">
                  {{ error }}
                </div>
              </div>
            </div>

            <!-- Chat Messages -->
            <div class="flex-1 overflow-y-auto p-6 space-y-4" ref="chatContainer">
              
              <div v-for="(message, idx) in conversationHistory" :key="idx" class="flex items-start gap-3">
                <div :class="message.sender === 'assistant' ? 'w-8 h-8 rounded-full bg-gradient-neon flex items-center justify-center flex-shrink-0 shadow-lg shadow-tribal-lime/50' : 'w-8 h-8 rounded-full bg-gradient-accent flex items-center justify-center flex-shrink-0 shadow-lg shadow-rust-red/50'">
                  <span class="text-sm font-semibold text-white">{{ message.sender === 'assistant' ? 'AI' : 'You' }}</span>
                </div>
                <div :class="message.sender === 'assistant' ? 'chat-bubble chat-bubble-assistant' : 'chat-bubble chat-bubble-user'">
                  <p>{{ message.message }}</p>
                </div>
              </div>

              <!-- Guided Assistant Response -->
              <div v-if="assistantMessage && !profileComplete" class="flex items-start gap-3">
                <div class="w-8 h-8 rounded-full bg-gradient-neon flex items-center justify-center flex-shrink-0 shadow-lg shadow-tribal-lime/50">
                  <span class="text-sm font-semibold text-white">AI</span>
                </div>
                <div class="chat-bubble chat-bubble-assistant">
                  <p>{{ assistantMessage }}</p>
                  <div v-if="currentContext" class="mt-3">
                    <p class="text-sm text-gray-400 mb-2">Building your profile...</p>
                    <div class="flex flex-wrap gap-2">
                      <span class="text-xs px-2 py-1 rounded-full bg-tribal-lime/20 text-tribal-lime">
                        {{ currentContext }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Final Profile and Recommendations (when complete) -->
              <div v-if="profileComplete && culturalProfile" class="flex items-start gap-3 animate-fade-in">
                <div class="w-8 h-8 rounded-full bg-gradient-neon flex items-center justify-center flex-shrink-0 shadow-lg shadow-tribal-lime/50">
                  <span class="text-sm font-semibold text-white">AI</span>
                </div>
                <div class="chat-bubble chat-bubble-assistant">
                  <p class="mb-2 font-semibold text-lg">{{ fullCulturalProfile.identity }}</p>
                  <p class="mb-4 text-sm text-gray-300">{{ fullCulturalProfile.description }}</p>
                  <p class="mb-2 font-medium">Music: <span class="font-normal">{{ culturalProfile.music.join(', ') }}</span></p>
                  <p class="mb-2 font-medium">Art: <span class="font-normal">{{ culturalProfile.art.join(', ') }}</span></p>
                  <p class="mb-2 font-medium">Fashion: <span class="font-normal">{{ culturalProfile.fashion.join(', ') }}</span></p>
                  <p class="mb-2 font-medium">Values: <span class="font-normal">{{ culturalProfile.values.join(', ') }}</span></p>
                  <p class="mb-2 font-medium">Places: <span class="font-normal">{{ culturalProfile.places.join(', ') }}</span></p>
                  <p class="mb-2 font-medium">Audiences: <span class="font-normal">{{ culturalProfile.audiences.join(', ') }}</span></p>
                  <p class="mt-4 font-semibold">Here are your personalized recommendations below!</p>
                </div>
              </div>
              
            </div>

            <!-- Chat Input -->
            <div class="p-6 border-t border-default">
              <form @submit.prevent="handleSubmit" class="flex gap-3">
                <div class="flex-1">
                  <textarea
                    v-model="userInput"
                    :disabled="isLoading"
                    placeholder="Tell me about your music taste, style, values, interests..."
                    rows="2"
                    class="input-field resize-none"
                    @keydown.enter.prevent="handleSubmit"
                  />
                </div>
                <button
                  type="submit"
                  :disabled="!userInput.trim() || isLoading"
                  class="btn btn-primary px-6 self-end"
                >
                  <span v-if="isLoading">
                    <div class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  </span>
                  <span v-else>Send</span>
                </button>
              </form>
              
              <!-- Quick Examples -->
              <div class="mt-3 flex flex-wrap gap-2">
                <span class="text-xs text-gray-400">Try:</span>
                <button 
                  v-for="example in examples" 
                  :key="example"
                  @click="addExample(example)"
                  class="chip chip-default text-xs"
                  :disabled="isLoading"
                >
                  {{ example }}
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Results Panel -->
        <div class="flex flex-col gap-6">
          
          <!-- Instructions Card -->
          <InstructionsCard v-if="!hasRecommendations" />

          <!-- Profile Display -->
          <ProfileDisplay 
            v-if="profileComplete && fullCulturalProfile"
            :profile="fullCulturalProfile"
            class="animate-fade-in"
          />

          <!-- Unified Recommendations Card -->
          <UnifiedRecommendationsCard
            v-if="profileComplete && recommendations"
            :recommendations="(recommendations as unknown as Record<string, any[]>)"
          />

          <!-- Answers Summary -->
          <AnswersSummary 
            v-if="userInput"
            :user-input="userInput"
            :cultural-profile="fullCulturalProfile"
          />

          <!-- Cultural Compatibility -->
          <CulturalCompatibility 
            v-if="profileComplete && matching"
            :matching="{...matching, shared_interests: [...matching.shared_interests]}"
            class="animate-fade-in"
            style="animation-delay: 0.4s"
          />

          <!-- Action Button -->
          <div v-if="hasRecommendations" class="animate-fade-in" style="animation-delay: 0.6s">
            <button
              @click="resetConversation"
              class="btn btn-accent w-full"
            >
              <AppIcon name="refresh" :size="16" />
              Start New Conversation
            </button>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, nextTick, computed } from 'vue';
import AppLayout from '@/components/layout/AppLayout.vue';
import AppIcon from '@/components/ui/AppIcon.vue';
import ProfileDisplay from '@/components/sections/ProfileDisplay.vue';
import UnifiedRecommendationsCard from '@/components/sections/UnifiedRecommendationsCard.vue';
import AnswersSummary from '@/components/sections/AnswersSummary.vue';
import CulturalCompatibility from '@/components/sections/CulturalCompatibility.vue';
import InstructionsCard from '@/components/sections/InstructionsCard.vue';
import { useConversation } from '@/composables/useConversation';

const conversation = useConversation();
const {
  isLoading,
  error,
  conversationHistory,
  currentContext,
  profileComplete,
  assistantMessage,
  culturalProfile,
  recommendations,
  matching,
  recommendationContext,
  hasRecommendations,
  processInput,
  resetConversation,
  fullCulturalProfile,
  userInput
} = conversation;
const chatContainer = ref<HTMLElement>();

const examples = [
  'Indie Rock',
  'Minimalism', 
  'Street Art',
  'Sustainability',
  'Urban Culture',
  'Vintage Style'
];

const handleSubmit = async () => {
  if (!userInput.value.trim()) return;
  try {
    await processInput(userInput.value.trim());
    userInput.value = '';
    await nextTick();
    if (chatContainer.value) {
      chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
    }
  } catch (err) {
    console.error('Error processing input:', err);
  }
};

const addExample = (example: string) => {
  if (!userInput.value.includes(example)) {
    userInput.value += (userInput.value ? ', ' : '') + example;
  }
};

const getRecommendationTitle = (context: string) => {
  switch (context) {
    case 'early':
      return 'Discover Your Style';
    case 'mid':
      return 'Building Your Profile';
    case 'complete':
      return 'Your Perfect Matches';
    default:
      return 'Recommendations';
  }
};

const getRecommendationDescription = (context: string) => {
  switch (context) {
    case 'early':
      return 'Here are some popular brands and places to get you started on your cultural journey.';
    case 'mid':
      return 'Based on what you\'ve shared, here are some recommendations that might interest you.';
    case 'complete':
      return 'Here are your personalized recommendations based on your complete cultural profile.';
    default:
      return 'Discover brands and places that match your cultural preferences.';
  }
};

const getContextLabel = (context: string) => {
  switch (context) {
    case 'early':
      return 'Early Discovery';
    case 'mid':
      return 'Building Profile';
    case 'complete':
      return 'Complete Profile';
    default:
      return 'Recommendations';
  }
};
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>