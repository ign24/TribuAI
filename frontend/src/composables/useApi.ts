import { ref, computed } from 'vue';
import { api } from '@/services/api';
import type { ApiResponse, CulturalProfileRequest } from '@/types';

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
      const response = await api.processInput(input);
      data.value = response;
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'An error occurred';
      console.error('API Error:', err);
    } finally {
      loading.value = false;
    }
  };

  const processProfile = async (profile: CulturalProfileRequest) => {
    loading.value = true;
    error.value = null;
    
    try {
      const response = await api.processProfile(profile);
      data.value = response;
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'An error occurred';
      console.error('API Error:', err);
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
    processProfile,
    reset
  };
}