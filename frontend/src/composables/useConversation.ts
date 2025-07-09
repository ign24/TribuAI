import { ref, computed } from 'vue';

export interface CulturalEntity {
  music?: string[];
  art?: string[];
  fashion?: string[];
  values?: string[];
  places?: string[];
  audiences?: string[];
}

export interface ConversationState {
  currentStep: number;
  entities: CulturalEntity;
  isComplete: boolean;
}

// Predefined questions for each cultural category
const CONVERSATION_FLOW = [
  {
    id: 'music',
    question: "🎵 What kind of music do you love? (e.g., indie rock, jazz, electronic, classical, hip-hop...)",
    placeholder: "Tell me about your favorite music genres, artists, or songs..."
  },
  {
    id: 'art',
    question: "🎨 What art forms inspire you? (e.g., cinema, photography, painting, sculpture, digital art...)",
    placeholder: "Share your favorite artists, films, or creative expressions..."
  },
  {
    id: 'fashion',
    question: "👗 How would you describe your style? (e.g., minimalist, vintage, streetwear, elegant, bohemian...)",
    placeholder: "Tell me about your fashion preferences and style choices..."
  },
  {
    id: 'values',
    question: "💎 What values are most important to you? (e.g., authenticity, sustainability, creativity, community...)",
    placeholder: "What principles guide your choices and lifestyle?"
  },
  {
    id: 'places',
    question: "🌍 What places or environments do you love? (e.g., cities, nature, cafes, galleries, markets...)",
    placeholder: "Tell me about your favorite places to visit or spend time..."
  },
  {
    id: 'audiences',
    question: "👥 What communities or groups do you identify with? (e.g., creatives, entrepreneurs, travelers, activists...)",
    placeholder: "What groups or communities do you feel connected to?"
  }
];

export function useConversation() {
  const currentStep = ref(0);
  const entities = ref<CulturalEntity>({});
  const isComplete = ref(false);
  const isLoading = ref(false);

  // Get current question
  const currentQuestion = computed(() => {
    if (currentStep.value >= CONVERSATION_FLOW.length) {
      return null;
    }
    return CONVERSATION_FLOW[currentStep.value];
  });

  // Check if we have enough information to proceed
  const hasEnoughInfo = computed(() => {
    const filledCategories = Object.values(entities.value).filter(arr => 
      Array.isArray(arr) && arr.length > 0
    ).length;
    return filledCategories >= 3; // Need at least 3 categories with data
  });

  // Process user response and determine next step
  const processResponse = (userInput: string) => {
    if (!currentQuestion.value) return;

    const category = currentQuestion.value.id as keyof CulturalEntity;
    
    // Extract entities from user input (simple keyword extraction)
    const extractedEntities = extractEntitiesFromInput(userInput, category);
    
    if (extractedEntities.length > 0) {
      entities.value[category] = extractedEntities;
    }

    // Move to next question
    currentStep.value++;

    // Check if we have enough information
    if (hasEnoughInfo.value || currentStep.value >= CONVERSATION_FLOW.length) {
      isComplete.value = true;
    }
  };

  // Simple entity extraction (in a real app, this could be more sophisticated)
  const extractEntitiesFromInput = (input: string, category: string): string[] => {
    const lowerInput = input.toLowerCase();
    const entities: string[] = [];

    // Extract based on category
    switch (category) {
      case 'music':
        const musicKeywords = ['rock', 'jazz', 'electronic', 'classical', 'hip-hop', 'indie', 'pop', 'folk', 'blues', 'reggae', 'country'];
        musicKeywords.forEach(keyword => {
          if (lowerInput.includes(keyword)) entities.push(keyword);
        });
        break;
      case 'art':
        const artKeywords = ['cinema', 'photography', 'painting', 'sculpture', 'digital art', 'theater', 'dance', 'literature', 'poetry'];
        artKeywords.forEach(keyword => {
          if (lowerInput.includes(keyword)) entities.push(keyword);
        });
        break;
      case 'fashion':
        const fashionKeywords = ['minimalist', 'vintage', 'streetwear', 'elegant', 'bohemian', 'casual', 'formal', 'sustainable', 'luxury'];
        fashionKeywords.forEach(keyword => {
          if (lowerInput.includes(keyword)) entities.push(keyword);
        });
        break;
      case 'values':
        const valueKeywords = ['authenticity', 'sustainability', 'creativity', 'community', 'innovation', 'tradition', 'freedom', 'equality', 'growth'];
        valueKeywords.forEach(keyword => {
          if (lowerInput.includes(keyword)) entities.push(keyword);
        });
        break;
      case 'places':
        const placeKeywords = ['cities', 'nature', 'cafes', 'galleries', 'markets', 'parks', 'museums', 'beaches', 'mountains'];
        placeKeywords.forEach(keyword => {
          if (lowerInput.includes(keyword)) entities.push(keyword);
        });
        break;
      case 'audiences':
        const audienceKeywords = ['creatives', 'entrepreneurs', 'travelers', 'activists', 'professionals', 'students', 'artists', 'designers'];
        audienceKeywords.forEach(keyword => {
          if (lowerInput.includes(keyword)) entities.push(keyword);
        });
        break;
    }

    // If no keywords found, add the input as a custom entity
    if (entities.length === 0 && input.trim()) {
      entities.push(input.trim());
    }

    return entities;
  };

  // Get next question or completion message
  const getNextMessage = () => {
    if (isComplete.value) {
      return {
        role: 'assistant' as const,
        content: `🎉 Perfect! I have enough information to create your cultural profile. Let me analyze your preferences and show you personalized recommendations.`
      };
    }

    if (currentQuestion.value) {
      return {
        role: 'assistant' as const,
        content: currentQuestion.value.question
      };
    }

    return {
      role: 'assistant' as const,
      content: "Thank you for sharing! Let me process your cultural profile."
    };
  };

  // Reset conversation
  const resetConversation = () => {
    currentStep.value = 0;
    entities.value = {};
    isComplete.value = false;
    isLoading.value = false;
  };

  return {
    currentStep,
    entities,
    isComplete,
    isLoading,
    currentQuestion,
    hasEnoughInfo,
    processResponse,
    getNextMessage,
    resetConversation,
    CONVERSATION_FLOW
  };
} 