export interface CulturalProfile {
  identity: string;
  description: string;
  music: string[];
  style: string[];
}

export interface EnrichedEntity {
  name: string;
  entity_id: string;
  description: string;
  image: string;
  tags: string[];
}

export interface Recommendations {
  brands: (EnrichedEntity | string)[];
  places: (EnrichedEntity | string)[];
}

export interface Matching {
  affinity_percentage: number;
  shared_interests: string[];
  audience_cluster: string;
}

export interface ApiResponse {
  cultural_profile: CulturalProfile;
  recommendations: Recommendations;
  matching: Matching;
}

export interface StatusResponse {
  status: string;
}

export interface HealthResponse {
  status: string;
}

export interface ProcessRequest {
  user_input: string;
}