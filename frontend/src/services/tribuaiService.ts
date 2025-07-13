import type { CulturalProfile, ApiResponse, ProcessResponse } from '@/types/tribuai'

const API_BASE_URL = 'http://localhost:8000'

export class TribuAIService {
  private static instance: TribuAIService
  private conversationHistory: Array<{ userInput: string; timestamp: string }> = []
  private currentContext: string = ''
  private profileComplete: boolean = false

  private constructor() {}

  static getInstance(): TribuAIService {
    if (!TribuAIService.instance) {
      TribuAIService.instance = new TribuAIService()
    }
    return TribuAIService.instance
  }

  /**
   * Process user input through LangGraph with dynamic recommendations
   */
  async processInput(userInput: string): Promise<ProcessResponse> {
    try {
      console.log('🔄 Processing input:', userInput)

      const response = await fetch(`${API_BASE_URL}/api/process`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_input: userInput }),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const result: ProcessResponse = await response.json()
      
      // Update conversation state
      this.conversationHistory.push({
        userInput,
        timestamp: new Date().toISOString()
      })
      
      if (result.current_context) {
        this.currentContext = result.current_context
      }
      
      if (result.profile_complete !== undefined) {
        this.profileComplete = result.profile_complete
      }

      console.log('✅ Processed input successfully:', {
        assistantMessage: result.assistant_message,
        profileComplete: result.profile_complete,
        context: result.current_context
      })

      return result
    } catch (error) {
      console.error('❌ Error processing input:', error)
      throw error
    }
  }

  /**
   * Process complete cultural profile (for when profile is complete)
   */
  async processCompleteProfile(profile: CulturalProfile): Promise<ApiResponse> {
    try {
      console.log('🎯 Processing complete profile:', profile)

      const response = await fetch(`${API_BASE_URL}/api/process-profile`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(profile),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const result: ApiResponse = await response.json()
      
      console.log('✅ Processed complete profile successfully')
      return result
    } catch (error) {
      console.error('❌ Error processing complete profile:', error)
      throw error
    }
  }

  /**
   * Get conversation history
   */
  getConversationHistory() {
    return this.conversationHistory
  }

  /**
   * Get current conversation context
   */
  getCurrentContext(): string {
    return this.currentContext
  }

  /**
   * Check if profile is complete
   */
  isProfileComplete(): boolean {
    return this.profileComplete
  }

  /**
   * Reset conversation state
   */
  resetConversation() {
    this.conversationHistory = []
    this.currentContext = ''
    this.profileComplete = false
    console.log('🔄 Conversation state reset')
  }

  /**
   * Get recommendation context based on conversation progress
   */
  getRecommendationContext(): string {
    const historyLength = this.conversationHistory.length
    
    if (historyLength <= 2) {
      return 'early'
    } else if (!this.profileComplete) {
      return 'mid'
    } else {
      return 'complete'
    }
  }

  /**
   * Health check for API
   */
  async healthCheck(): Promise<boolean> {
    try {
      const response = await fetch(`${API_BASE_URL}/health`)
      return response.ok
    } catch (error) {
      console.error('❌ Health check failed:', error)
      return false
    }
  }
}

export default TribuAIService.getInstance() 