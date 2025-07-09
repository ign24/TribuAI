<template>
  <div class="max-w-2xl mx-auto px-6">
    <AppCard class="text-center mb-8">
      <h2 class="text-2xl font-semibold mb-4 text-soft-white">
        Tell us about your cultural preferences
      </h2>
      <p class="text-gray-300 mb-6">
        You are not just a consumer. You're a cultural node. Let's discover your tribe.
      </p>
      
      <form @submit.prevent="handleSubmit" class="space-y-6">
        <div class="text-left">
          <label for="cultural-input" class="block text-sm font-medium text-gray-300 mb-2">
            What resonates with you culturally?
          </label>
          <textarea
            id="cultural-input"
            v-model="userInput"
            :disabled="loading"
            placeholder="Tell us about your music taste, style preferences, values, interests... For example: 'I love indie rock, street art, and sustainable fashion. I value authenticity and creative expression.'"
            rows="6"
            class="w-full px-4 py-3 bg-gray-800/50 border border-gray-600 rounded-lg text-soft-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-tribal-lime focus:border-transparent transition-all duration-200 backdrop-blur-sm"
          />
        </div>
        
        <div class="flex flex-wrap gap-2 justify-center">
          <span class="text-sm text-gray-400">Examples:</span>
          <AppChip
            v-for="example in examples"
            :key="example"
            variant="secondary"
            size="sm"
            class="cursor-pointer hover:bg-slate-blue/30"
            @click="addExample(example)"
          >
            {{ example }}
          </AppChip>
        </div>
        
        <AppButton
          type="submit"
          :loading="loading"
          :disabled="!userInput.trim() || loading"
          variant="primary"
          size="lg"
          full-width
        >
          {{ loading ? 'Analyzing your tribe...' : 'Discover My Tribe' }}
        </AppButton>
      </form>
    </AppCard>
    
    <div class="text-center text-gray-400 text-sm">
      <p>Powered by cultural intelligence • Privacy first</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import AppCard from '@/components/ui/AppCard.vue';
import AppButton from '@/components/ui/AppButton.vue';
import AppChip from '@/components/ui/AppChip.vue';

interface Props {
  loading?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  loading: false
});

const emit = defineEmits<{
  submit: [input: string];
}>();

const userInput = ref('');

const examples = [
  'Indie Rock',
  'Minimalism',
  'Street Art',
  'Sustainable Fashion',
  'Craft Coffee',
  'Vintage Aesthetics',
  'Tech Innovation',
  'Urban Exploration'
];

const handleSubmit = () => {
  if (userInput.value.trim()) {
    emit('submit', userInput.value.trim());
  }
};

const addExample = (example: string) => {
  if (!userInput.value.includes(example)) {
    userInput.value += (userInput.value ? ', ' : '') + example;
  }
};
</script>