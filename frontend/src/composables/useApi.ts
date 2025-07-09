import { ref, computed } from 'vue';
import { api } from '@/services/api';
import type { ApiResponse, ProcessRequest } from '@/types';

export interface CulturalProfile {
  music: string[];
  art: string[];
  fashion: string[];
  values: string[];
  places: string[];
  audiences: string[];
}

export function useApi() {
  const loading = ref(false);
  const error = ref<string | null>(null);
  const data = ref<ApiResponse | null>(null);

  const isLoading = computed(() => loading.value);
  const hasError = computed(() => error.value !== null);
  const hasData = computed(() => data.value !== null);

  const processInput = async (input: string) => {
    loading.value = true;
    error.value = null;
    
    try {
      const request: ProcessRequest = { user_input: input };
      const response = await api.processInput(request);
      data.value = response;
      console.log('[TribuAI] API response:', response);
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'An error occurred';
    } finally {
      loading.value = false;
    }
  };

  const processCulturalProfile = async (profile: CulturalProfile) => {
    loading.value = true;
    error.value = null;
    
    try {
      console.log('[TribuAI] Processing cultural profile:', profile);
      const response = await api.processCulturalProfile(profile);
      data.value = response;
      console.log('[TribuAI] Cultural profile processed successfully:', response);
      console.log('[TribuAI] Cultural profile details:', response.cultural_profile);
      console.log('[TribuAI] Recommendations:', response.recommendations);
      console.log('[TribuAI] Matching info:', response.matching);
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'An error occurred';
      console.error('[TribuAI] Error processing cultural profile:', err);
    } finally {
      loading.value = false;
    }
  };

  const reset = () => {
    loading.value = false;
    error.value = null;
    data.value = null;
  };

  return {
    loading: isLoading,
    error: hasError,
    errorMessage: computed(() => error.value),
    data: computed(() => data.value),
    hasData,
    processInput,
    processCulturalProfile,
    reset
  };
}