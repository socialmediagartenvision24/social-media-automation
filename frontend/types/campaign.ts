import type { SocialPlatform } from "./account";

export type CampaignStatus =
  | "draft"
  | "active"
  | "paused"
  | "completed"
  | "archived";

export type ScheduleMode =
  | "fixed"
  | "interval";

export interface CampaignSchedule {
  mode: ScheduleMode;

  timezone: string;

  startDate: string;

  endDate?: string | null;

  postsPerDay: number;

  intervalMinutes?: number | null;

  postingTimes?: string[];

  repeatEnabled: boolean;

  repeatIntervalDays?: number | null;
}

export interface CampaignAccount {
  accountId: string;

  platform: SocialPlatform;
}

export interface CampaignVideo {
  videoId: string;

  position: number;

  enabled: boolean;
}

export interface Campaign {
  id: string;

  name: string;

  description?: string | null;

  status: CampaignStatus;

  accountCount: number;

  videoCount: number;

  postsPerDay: number;

  loopEnabled: boolean;

  schedule: CampaignSchedule;

  accounts?: CampaignAccount[];

  videos?: CampaignVideo[];

  createdAt: string;

  updatedAt: string;
}

export interface CreateCampaignInput {
  name: string;

  description?: string;

  accountIds: string[];

  videoIds: string[];

  schedule: CampaignSchedule;
}

export interface UpdateCampaignInput {
  name?: string;

  description?: string;

  status?: CampaignStatus;

  accountIds?: string[];

  videoIds?: string[];

  schedule?: Partial<CampaignSchedule>;
}
