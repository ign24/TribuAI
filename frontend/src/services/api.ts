import type { ApiResponse, StatusResponse, HealthResponse } from '@/types';

const BASE_URL = 'http://localhost:8000'; // Backend URL

export const api = {
  async processInput(userInput: string): Promise<ApiResponse> {
    const response = await fetch(`${BASE_URL}/api/process`, {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({ user_input: userInput })
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`API Error: ${response.status} - ${errorText}`);
    }

    return response.json();
  },

  async processProfile(profile: any): Promise<ApiResponse> {
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
      throw new Error(`API Error: ${response.status} - ${errorText}`);
    }

    return response.json();
  },

  async getStatus(): Promise<StatusResponse> {
    const response = await fetch(`${BASE_URL}/status`);
    
    if (!response.ok) {
      throw new Error(`Status check failed: ${response.status}`);
    }

    return response.json();
  },

  async getHealth(): Promise<HealthResponse> {
    const response = await fetch(`${BASE_URL}/health`);
    
    if (!response.ok) {
      throw new Error(`Health check failed: ${response.status}`);
    }

    return response.json();
  }
};