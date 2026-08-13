export type SocialPlatform =
  | "instagram"
  | "facebook"
  | "tiktok";

export type AccountStatus =
  | "connected"
  | "disconnected"
  | "expired"
  | "error";

export interface SocialAccount {
  id: string;

  name: string;

  username?: string | null;

  platform: SocialPlatform;

  status: AccountStatus;

  timezone: string;

  profileImageUrl?: string | null;

  platformAccountId?: string | null;

  createdAt: string;

  updatedAt: string;

  lastSyncedAt?: string | null;
}

export interface CreateAccountInput {
  name: string;

  platform: SocialPlatform;

  timezone?: string;
}

export interface UpdateAccountInput {
  name?: string;

  timezone?: string;

  status?: AccountStatus;
}
