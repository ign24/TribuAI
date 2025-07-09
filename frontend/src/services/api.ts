import type { ApiResponse, StatusResponse, HealthResponse, ProcessRequest } from '@/types';

export interface CulturalProfile {
  music: string[];
  art: string[];
  fashion: string[];
  values: string[];
  places: string[];
  audiences: string[];
}

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Simulate network delay
const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

export const api = {
  async processInput(data: ProcessRequest): Promise<ApiResponse> {
    try {
      console.log('Sending request to:', `${BASE_URL}/api/process`);
      
      const response = await fetch(`${BASE_URL}/api/process`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify(data)
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      console.log('API Response:', result);
      return result;
      
    } catch (error) {
      console.error('API Error:', error);
      
      throw error;
    }
  },

  async processCulturalProfile(profile: CulturalProfile): Promise<ApiResponse> {
    try {
      console.log('[TribuAI] Sending cultural profile to:', `${BASE_URL}/api/process-profile`);
      console.log('[TribuAI] Profile data:', profile);
      
      const response = await fetch(`${BASE_URL}/api/process-profile`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify(profile)
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error('[TribuAI] API Error Response:', errorText);
        throw new Error(`HTTP error! status: ${response.status}, body: ${errorText}`);
      }

      const result = await response.json();
      console.log('[TribuAI] Cultural Profile API Response:', result);
      console.log('[TribuAI] Response structure:', {
        hasCulturalProfile: !!result.cultural_profile,
        hasRecommendations: !!result.recommendations,
        hasMatching: !!result.matching,
        culturalProfileKeys: result.cultural_profile ? Object.keys(result.cultural_profile) : [],
        recommendationsKeys: result.recommendations ? Object.keys(result.recommendations) : []
      });
      return result;
      
    } catch (error) {
      console.error('[TribuAI] Cultural Profile API Error:', error);
      
      throw error;
    }
  },

  async getStatus(): Promise<StatusResponse> {
    try {
      const response = await fetch(`${BASE_URL}/status`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Status check error:', error);
      return { status: "unknown" };
    }
  },

  async getHealth(): Promise<HealthResponse> {
    try {
      const response = await fetch(`${BASE_URL}/health`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Health check error:', error);
      return { status: "unhealthy" };
    }
  }
};