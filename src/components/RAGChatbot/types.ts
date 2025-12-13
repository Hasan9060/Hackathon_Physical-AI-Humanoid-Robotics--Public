export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  sources?: ChatSource[];
  contextUsed?: boolean;
}

export interface ChatSource {
  file_path?: string;
  section?: string;
  score?: number;
  snippet?: string;
  type?: string;
  content?: string;
}

export interface ChatSession {
  session_id: string;
  last_message_at: string;
  message_count: number;
  metadata: any;
}

export interface IngestionStatus {
  status: string;
  total_files: number;
  processed_files: number;
  total_chunks: number;
  completion_percentage: number;
}