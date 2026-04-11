export interface AnalyzeRequest {
  input: string;
  mode?: 'auto' | 'url' | 'text';
  summary_length?: 'short' | 'medium' | 'detailed';
}

export interface Entity {
  people: string[];
  organizations: string[];
  locations: string[];
}

export interface AnalyzeResponse {
  title: string;
  source: string;
  language: string;
  article_text: string;
  reading_time_minutes: number;
  german_summary: string;
  english_summary: string;
  keywords: string[];
  entities: Entity;
  tone: string;
}

export interface ApiError {
  detail: string;
}
