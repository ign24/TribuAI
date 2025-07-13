export interface CulturalProfile {
  identity: string;
  description: string;
  music: string[];
  style: string[];
}

export interface BrandRecommendation {
  name: string;
  entity_id: string;
  description: string;
  image: string;
  tags: string[];
}

export interface PlaceRecommendation {
  name: string;
  entity_id: string;
  description: string;
  image: string;
  tags: string[];
}

export interface Recommendations {
  [key: string]: BrandRecommendation[] | PlaceRecommendation[] | any[];
}

export interface Matching {
  affinity_percentage: number;
  shared_interests: string[];
  audience_cluster: string;
}

export interface ApiResponse {
  cultural_profile: CulturalProfile;
  recommendations: Recommendations;
  matching?: Matching;
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

export interface CulturalProfileRequest {
  music: string[];
  art: string[];
  fashion: string[];
  values: string[];
  places: string[];
  audiences: string[];
}