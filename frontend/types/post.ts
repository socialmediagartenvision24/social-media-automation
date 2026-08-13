import type { SocialPlatform } from "./account";

export type PostStatus =
  | "scheduled"
  | "pending"
  | "processing"
  | "published"
  | "failed"
  | "cancelled";

export interface Post {
  id: string;

  campaignId?: string | null;

  accountId: string;

  videoId: string;

  platform: SocialPlatform;

  status: PostStatus;

  scheduledAt: string;

  publishedAt?: string | null;

  externalPostId?: string | null;

  externalPostUrl?: string | null;

  errorMessage?: string | null;

  retryCount: number;

  maxRetries: number;

  createdAt: string;

  updatedAt: string;
}

export interface CreatePostInput {
  campaignId?: string;

  accountId: string;

  videoId: string;

  platform: SocialPlatform;

  scheduledAt: string;

  maxRetries?: number;
}

export interface UpdatePostInput {
  status?: PostStatus;

  scheduledAt?: string;

  errorMessage?: string | null;
}

export interface QueueStats {
  pending: number;

  processing: number;

  published: number;

  failed: number;

  scheduled: number;

  cancelled: number;
}
