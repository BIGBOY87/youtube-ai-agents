export type AgentType = 'ANALYST' | 'SHORTS_DIRECTOR' | 'SEO_OPTIMIZER' | 'COMMUNITY_MANAGER' | 'SYSTEM_RECOVERY' | 'MARKETING_AGENT';

export interface VideoItem {
  id: string;
  title: string;
  description: string;
  type: 'Short' | 'Standard';
  status: 'Published' | 'Draft' | 'Scheduled' | 'ReviewNeeded';
  views: number;
  likes: number;
  ctr: number; // Click-Through Rate in %
  averageViewDuration: number; // in seconds
  publishDate: string;
  duration: number; // in seconds
  thumbnailUrl?: string;
  scriptIdea?: string;
  visualPrompts?: string[];
  optimizedTitles?: string[];
  originalTitle?: string;
  optimizationResult?: string;
}

export interface YouTubeComment {
  id: string;
  videoId: string;
  videoTitle: string;
  author: string;
  authorAvatar?: string;
  text: string;
  publishedAt: string;
  sentiment: 'Positive' | 'Neutral' | 'Negative';
  replyStatus: 'Unreplied' | 'Generating' | 'Replied';
  agentReplyDraft?: string;
  actualReply?: string;
}

export interface AgentActivityLog {
  id: string;
  agent: AgentType;
  action: string;
  timestamp: string;
  impact: 'Info' | 'Success' | 'Warning' | 'Optimization';
  details?: string;
}

export interface AgentMessage {
  id: string;
  sender: AgentType;
  recipient: AgentType | 'ALL';
  message: string;
  timestamp: string;
  contextData?: any;
}

export interface ChartDataPoint {
  date: string;
  views: number;
  subscribers: number;
  watchTime: number;
  ctr: number;
}

export interface ChannelStats {
  totalViews: number;
  subscriberCount: number;
  totalWatchTime: number; // in hours
  avgCtr: number; // %
  trendData: ChartDataPoint[];
}

export interface AgentConfig {
  AUTONOMY_ENABLED: boolean;
  AUTO_APPROVE_UPLOADS: boolean;
  AUTO_PUBLIC_MODE: boolean;
  AUTO_REPLY_MODE: boolean;
  AUTO_SCHEDULER_ENABLED: boolean;
  AUTO_UPLOAD: boolean;
  AUTO_VIDEO_SECONDS: number;
  DEFAULT_UPLOAD_PRIVACY: 'public' | 'unlisted' | 'private';
  DRIVE_MATCH_THRESHOLD: number;
  DRIVE_SOURCE_FOLDER_ID: string;
  YOUTUBE_CHANNEL_ID: string;
  YOUTUBE_UPLOAD_ENABLED: boolean;
  GOOGLE_API_KEY_PRESENT: boolean;
  OPENAI_API_KEY_PRESENT: boolean;
  YOUTUBE_API_KEY_PRESENT: boolean;
  YOUTUBE_CLIENT_ID?: string;
  YOUTUBE_CLIENT_SECRET?: string;
  YOUTUBE_REFRESH_TOKEN?: string;
  GOOGLE_API_KEY?: string;
}
