import { ref, computed, readonly } from 'vue'
import type { ApiResponse, CulturalProfile } from '@/types/tribuai'
import tribuaiService from '@/services/tribuaiService'

const fullCulturalProfile = ref<any>(null)
const userInput = ref('');

export function useConversation() {
  // Reactive state
  const isLoading = ref(false)
  const error = ref<string | null>(null)
  // Place these at the top, only once
  const initialAssistantMessage = "Hi! I'm here to help you discover your cultural identity. Tell me about your interests, and I'll guide you step by step.";
  const conversationHistory = ref<Array<{ sender: 'user' | 'assistant'; message: string }>>([
    { sender: 'assistant', message: initialAssistantMessage }
  ]);
  const currentContext = ref('')
  const profileComplete = ref(false)
  const assistantMessage = ref('')
  
  // Cultural profile state
  const culturalProfile = ref<CulturalProfile>({
    music: [],
    art: [],
    fashion: [],
    values: [],
    places: [],
    audiences: []
  })
  
  // Recommendations state
  const recommendations = ref<Record<string, any[]>>({})
  
  // Matching state
  const matching = ref<{
    affinity_percentage: number
    shared_interests: string[]
    audience_cluster: string
  } | null>(null)

  // Computed properties
  const recommendationContext = computed(() => {
    const historyLength = conversationHistory.value.length
    
    if (historyLength <= 2) {
      return 'early'
    } else if (!profileComplete.value) {
      return 'mid'
    } else {
      return 'complete'
    }
  })

  // Update conversationState to use the new structure
  const conversationState = computed(() => ({
    history: conversationHistory.value,
    currentContext: currentContext.value,
    profileComplete: profileComplete.value,
    recommendationContext: recommendationContext.value
  }));

  const hasRecommendations = computed(() => {
    return Object.values(recommendations.value).some(arr => arr.length > 0)
  })

  const isProfileInProgress = computed(() => {
    const requiredFields = ['music', 'art', 'fashion', 'values', 'places', 'audiences']
    return requiredFields.some(field => 
      culturalProfile.value[field as keyof CulturalProfile].length === 0
    )
  })

  // Remove profileSteps and getNextAssistantQuestion logic
  // Only keep conversationHistory, processInput, and backend call logic

  async function processInput(userMessage: string) {
    isLoading.value = true;
    error.value = '';
    // Only add the user's message, not the initial assistant message
    conversationHistory.value.push({ sender: 'user', message: userMessage });
    try {
      const result = await tribuaiService.processInput(userMessage);
      
      // Update assistant message
      if (result.assistant_message) {
        conversationHistory.value.push({ sender: 'assistant', message: result.assistant_message });
      }
      
      // Update cultural profile
      if (result.cultural_profile) {
        fullCulturalProfile.value = result.cultural_profile;
      }
      
      // Update profile completion status
      if (result.profile_complete !== undefined) {
        profileComplete.value = result.profile_complete;
      }
      
      // Update current context
      if (result.current_context) {
        currentContext.value = result.current_context;
      }
      
      // Update recommendations if they exist
      if (result.recommendations) {
        recommendations.value = result.recommendations;
        console.log('✅ Updated recommendations:', result.recommendations);
      }
      
      console.log('✅ Processed input successfully:', {
        assistantMessage: result.assistant_message,
        profileComplete: result.profile_complete,
        recommendations: result.recommendations
      });
      
    } catch (e: any) {
      error.value = e.message || 'Error processing input';
      console.error('❌ Error processing input:', e);
    } finally {
      isLoading.value = false;
    }
  }

  const processCompleteProfile = async (): Promise<ApiResponse> => {
    if (!profileComplete.value) {
      throw new Error('Profile is not complete yet')
    }
    
    isLoading.value = true
    error.value = null
    
    try {
      console.log('🎯 Processing complete profile')
      
      const result = await tribuaiService.processCompleteProfile(culturalProfile.value)
      
      // Update recommendations with comprehensive data
      if (result.recommendations) {
        recommendations.value = result.recommendations
      }
      
      // Update matching information
      if (result.matching) {
        matching.value = result.matching
      }
      
      console.log('✅ Complete profile processed successfully')
      
      return result
      
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error occurred'
      error.value = errorMessage
      console.error('❌ Error processing complete profile:', err)
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const resetConversation = () => {
    console.log('🔄 Resetting conversation state')
    
    isLoading.value = false
    error.value = null
    conversationHistory.value = []
    currentContext.value = ''
    profileComplete.value = false
    assistantMessage.value = ''
    
    culturalProfile.value = {
      music: [],
      art: [],
      fashion: [],
      values: [],
      places: [],
      audiences: []
    };
    
    recommendations.value = {}
    
    matching.value = null
    
    tribuaiService.resetConversation()
  }

  return {
    // State
    isLoading: readonly(isLoading),
    error: readonly(error),
    conversationHistory: readonly(conversationHistory),
    currentContext: readonly(currentContext),
    profileComplete: readonly(profileComplete),
    assistantMessage: readonly(assistantMessage),
    culturalProfile: readonly(culturalProfile),
    recommendations: readonly(recommendations),
    matching: readonly(matching),
    fullCulturalProfile: readonly(fullCulturalProfile),
    userInput,
    
    // Computed
    recommendationContext,
    conversationState,
    hasRecommendations,
    isProfileInProgress,
    
    // Methods
    processInput,
    processCompleteProfile,
    resetConversation
  }
} 