// Base types for cultural entities
export interface CulturalEntity {
  name: string
  description?: string
  image?: string
  tags?: string[]
}

// Cultural profile structure
export interface CulturalProfile {
  music: string[]
  art: string[]
  fashion: string[]
  values: string[]
  places: string[]
  audiences: string[]
}

// Full profile for API responses (includes identity and description)
export interface FullCulturalProfile extends CulturalProfile {
  identity: string
  description: string
}

// Recommendation structure with real Qloo data
export interface Recommendation {
  name: string
  entity_id: string
  description: string
  image: string
  tags: string[]
}

// API response for process endpoint (LangGraph flow)
export interface ProcessResponse {
  cultural_profile: FullCulturalProfile
  recommendations: {
    [key: string]: Recommendation[]
  }
  assistant_message?: string
  profile_complete?: boolean
  current_context?: string
  recommendation_context?: string
  conversation_history?: Array<{
    user_input: string
    timestamp: string
  }>
  processing_time?: number
  error_message?: string
}

// API response for complete profile processing
export interface ApiResponse {
  cultural_profile: FullCulturalProfile
  recommendations: {
    [key: string]: Recommendation[]
  }
  matching?: {
    affinity_percentage: number
    shared_interests: string[]
    audience_cluster: string
  }
}

// Conversation state for dynamic recommendations
export interface ConversationState {
  history: Array<{
    userInput: string
    timestamp: string
  }>
  currentContext: string
  profileComplete: boolean
  recommendationContext: 'early' | 'mid' | 'complete'
}

// Recommendation context types
export type RecommendationContext = 'early' | 'mid' | 'complete'

// UI state for recommendations
export interface RecommendationDisplay {
  context: RecommendationContext
  title: string
  description: string
  items: Recommendation[]
  loading: boolean
}

// Error types
export interface ApiError {
  message: string
  status: number
  details?: string
}

// Health check response
export interface HealthResponse {
  status: string
} 