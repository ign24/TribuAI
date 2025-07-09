<template>
  <AppLayout>
    <div class="flex flex-col md:flex-row max-w-6xl mx-auto px-4 py-8 gap-8">
      <!-- Chat Section -->
      <div class="flex-1 min-w-0">
        <div class="bg-gray-900 rounded-lg shadow-lg p-6 min-h-[400px] flex flex-col">
          <div class="flex-1 overflow-y-auto mb-4">
            <div v-for="(msg, idx) in chatHistory" :key="idx" class="mb-3">
              <div v-if="msg.role === 'user'" class="text-right">
                <div class="inline-block bg-slate-blue/80 text-white px-4 py-2 rounded-lg">
                  {{ msg.content }}
                </div>
              </div>
              <div v-else class="text-left">
                <div class="inline-block bg-gray-700/80 text-gray-100 px-4 py-2 rounded-lg whitespace-pre-line">
                  <span v-html="formatAssistantMessage(msg.content)"></span>
                </div>
              </div>
            </div>
          </div>
          <form @submit.prevent="sendMessage" class="flex gap-2 mt-auto">
            <input
              v-model="userInput"
              type="text"
              class="flex-1 rounded-lg px-4 py-2 bg-gray-800 text-white focus:outline-none"
              :placeholder="currentQuestion?.placeholder || 'Share your thoughts...'"
              autocomplete="off"
            />
            <AppButton type="submit" variant="primary" :disabled="loading || conversation.isLoading.value">
              {{ conversation.isComplete ? 'See Results' : 'Send' }}
            </AppButton>
          </form>
        </div>
      </div>
      <!-- Results Section -->
      <div v-if="api.data.value" class="w-full md:w-[400px] flex flex-col gap-6">
        <ProfileDisplay :profile="api.data.value.cultural_profile" />
        <BrandRecommendations :brands="api.data.value.recommendations.brands" />
        <GeographicAffinities :places="api.data.value.recommendations.places" />
        <CulturalCompatibility :matching="api.data.value.matching" />
      </div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, watch, computed, watchEffect, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import AppLayout from '@/components/layout/AppLayout.vue';
import AppButton from '@/components/ui/AppButton.vue';
import ProfileDisplay from '@/components/sections/ProfileDisplay.vue';
import BrandRecommendations from '@/components/sections/BrandRecommendations.vue';
import GeographicAffinities from '@/components/sections/GeographicAffinities.vue';
import CulturalCompatibility from '@/components/sections/CulturalCompatibility.vue';
import { useApi } from '@/composables/useApi';
import { useConversation } from '@/composables/useConversation';

const router = useRouter();
const api = useApi();
const conversation = useConversation();

const onboardingMessage = {
  role: 'assistant' as const,
  content: `👋 <b>Hi! I'm TribuAI, your cultural intelligence guide.</b><br><br>
I'll help you discover your unique cultural identity and recommend brands, places, and experiences that truly fit you.<br><br>
<b>How it works:</b><br>
<ul style='margin-left:1em;'>
  <li>I'll ask you a few questions about your tastes and preferences.</li>
  <li>Just answer naturally - there are no wrong answers!</li>
  <li>When we're done, I'll show you your personalized cultural profile and recommendations.</li>
</ul>
Ready? <b>Let's start!</b>`
};

const initialHistory = (() => {
  const stored = sessionStorage.getItem('tribuai_chat_history');
  if (stored) {
    const parsed = JSON.parse(stored);
    if (Array.isArray(parsed) && parsed.length === 0) {
      return [onboardingMessage];
    }
    return parsed;
  }
  return [onboardingMessage];
})();

const chatHistory = ref<{ role: 'user' | 'assistant'; content: string }[]>(initialHistory);
const userInput = ref('');
const loading = ref(false);
const hasRequestedProfile = ref(false); // Flag to prevent multiple requests

// Get current question from conversation system
const currentQuestion = computed(() => conversation.currentQuestion.value);

watch(chatHistory, (val) => {
  sessionStorage.setItem('tribuai_chat_history', JSON.stringify(val));
}, { deep: true });

// Add first question when component mounts
onMounted(() => {
  if (chatHistory.value.length === 1) {
    // Only add first question if we just have the onboarding message
    const firstQuestion = conversation.getNextMessage();
    chatHistory.value.push(firstQuestion);
  }
});

// Watch for conversation completion - only send request once
watchEffect(() => {
  if (conversation.isComplete.value && !loading.value && !hasRequestedProfile.value) {
    // Send complete profile to backend only once
    sendCompleteProfile();
    hasRequestedProfile.value = true; // Mark as requested
  }
});

function formatAssistantMessage(msg: string) {
  // If the message already contains HTML, return as is
  if (msg.includes('<ul') || msg.includes('<b>') || msg.includes('<br>')) return msg;
  // Simple formatting for other assistant messages
  return msg.replace(/\n/g, '<br>');
}

const sendMessage = async () => {
  if (!userInput.value.trim()) return;
  
  const userMessage = { role: 'user' as const, content: userInput.value };
  chatHistory.value.push(userMessage);
  
  const userInputText = userInput.value;
  userInput.value = '';
  loading.value = true;
  
  try {
    // Process response through conversation system
    conversation.processResponse(userInputText);
    
    // Get next message from conversation system
    const nextMessage = conversation.getNextMessage();
    chatHistory.value.push(nextMessage);
    
    // If conversation is complete, the watchEffect will handle sending to backend
    // No need to call sendCompleteProfile here as it's handled by the watcher
  } catch (e) {
    chatHistory.value.push({ 
      role: 'assistant', 
      content: 'An error occurred. Please try again.' 
    });
  } finally {
    loading.value = false;
  }
};

const sendCompleteProfile = async () => {
  if (loading.value) return;
  
  loading.value = true;
  try {
    // Convert conversation entities to the format expected by backend
    const culturalProfile = {
      music: conversation.entities.value.music || [],
      art: conversation.entities.value.art || [],
      fashion: conversation.entities.value.fashion || [],
      values: conversation.entities.value.values || [],
      places: conversation.entities.value.places || [],
      audiences: conversation.entities.value.audiences || []
    };
    // Send to backend for processing and recommendations
    await api.processCulturalProfile(culturalProfile);
    // Do NOT redirect to /results; show results in side panel
  } catch (e) {
    chatHistory.value.push({ 
      role: 'assistant', 
      content: 'An error occurred while processing your profile. Please try again.' 
    });
  } finally {
    loading.value = false;
  }
};

const canShowResults = computed(() => {
  return conversation.hasEnoughInfo.value;
});

const goToResults = () => {
  router.push('/results');
};

// Function to reset the conversation (for new chat)
const resetConversation = () => {
  hasRequestedProfile.value = false;
  conversation.resetConversation();
  chatHistory.value = [onboardingMessage];
  sessionStorage.removeItem('tribuai_chat_history');
};
</script>