-- ============================================================================
-- SOCIAL MEDIA AUTOMATION
-- Migration: 001_initial_schema.sql
-- ============================================================================

create extension if not exists "pgcrypto";

-- ============================================================================
-- ENUMS
-- ============================================================================

do $$
begin
  create type public.social_platform as enum (
    'instagram',
    'facebook',
    'tiktok'
  );
exception
  when duplicate_object then null;
end $$;

do $$
begin
  create type public.account_status as enum (
    'connected',
    'disconnected',
    'expired',
    'error'
  );
exception
  when duplicate_object then null;
end $$;

do $$
begin
  create type public.video_status as enum (
    'uploading',
    'processing',
    'ready',
    'failed',
    'deleted'
  );
exception
  when duplicate_object then null;
end $$;

do $$
begin
  create type public.campaign_status as enum (
    'draft',
    'active',
    'paused',
    'completed',
    'archived'
  );
exception
  when duplicate_object then null;
end $$;

do $$
begin
  create type public.post_status as enum (
    'scheduled',
    'pending',
    'processing',
    'published',
    'failed',
    'cancelled'
  );
exception
  when duplicate_object then null;
end $$;

do $$
begin
  create type public.job_status as enum (
    'pending',
    'processing',
    'completed',
    'failed',
    'cancelled'
  );
exception
  when duplicate_object then null;
end $$;

-- ============================================================================
-- UPDATED_AT FUNCTION
-- ============================================================================

create or replace function public.set_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

-- ============================================================================
-- PROFILES
-- ============================================================================

create table if not exists public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,

  email text,

  display_name text,

  avatar_url text,

  timezone text not null default 'Europe/Berlin',

  created_at timestamptz not null default now(),

  updated_at timestamptz not null default now()
);

create index if not exists profiles_email_idx
  on public.profiles(email);

drop trigger if exists profiles_updated_at on public.profiles;

create trigger profiles_updated_at
before update on public.profiles
for each row
execute function public.set_updated_at();

-- ============================================================================
-- SOCIAL ACCOUNTS
-- ============================================================================

create table if not exists public.social_accounts (
  id uuid primary key default gen_random_uuid(),

  user_id uuid not null
    references public.profiles(id)
    on delete cascade,

  platform public.social_platform not null,

  name text not null,

  username text,

  platform_account_id text,

  profile_image_url text,

  status public.account_status not null default 'disconnected',

  timezone text not null default 'Europe/Berlin',

  access_token_encrypted text,

  refresh_token_encrypted text,

  token_expires_at timestamptz,

  last_synced_at timestamptz,

  last_error text,

  created_at timestamptz not null default now(),

  updated_at timestamptz not null default now(),

  unique(user_id, platform, platform_account_id)
);

create index if not exists social_accounts_user_id_idx
  on public.social_accounts(user_id);

create index if not exists social_accounts_platform_idx
  on public.social_accounts(platform);

create index if not exists social_accounts_status_idx
  on public.social_accounts(status);

drop trigger if exists social_accounts_updated_at
on public.social_accounts;

create trigger social_accounts_updated_at
before update on public.social_accounts
for each row
execute function public.set_updated_at();

-- ============================================================================
-- VIDEOS
-- ============================================================================

create table if not exists public.videos (
  id uuid primary key default gen_random_uuid(),

  user_id uuid not null
    references public.profiles(id)
    on delete cascade,

  name text not null,

  description text,

  storage_path text not null,

  public_url text,

  thumbnail_url text,

  mime_type text not null,

  file_size_bytes bigint not null default 0,

  duration_seconds numeric(12,3) not null default 0,

  width integer,

  height integer,

  status public.video_status not null default 'uploading',

  processing_error text,

  created_at timestamptz not null default now(),

  updated_at timestamptz not null default now()
);

create index if not exists videos_user_id_idx
  on public.videos(user_id);

create index if not exists videos_status_idx
  on public.videos(status);

create index if not exists videos_created_at_idx
  on public.videos(created_at desc);

drop trigger if exists videos_updated_at on public.videos;

create trigger videos_updated_at
before update on public.videos
for each row
execute function public.set_updated_at();

-- ============================================================================
-- CAMPAIGNS
-- ============================================================================

create table if not exists public.campaigns (
  id uuid primary key default gen_random_uuid(),

  user_id uuid not null
    references public.profiles(id)
    on delete cascade,

  name text not null,

  description text,

  status public.campaign_status not null default 'draft',

  timezone text not null default 'Europe/Berlin',

  start_date date not null,

  end_date date,

  posts_per_day integer not null default 1,

  schedule_mode text not null default 'fixed',

  interval_minutes integer,

  posting_times jsonb not null default '[]'::jsonb,

  repeat_enabled boolean not null default false,

  repeat_interval_days integer,

  current_cycle integer not null default 1,

  created_at timestamptz not null default now(),

  updated_at timestamptz not null default now(),

  constraint campaigns_posts_per_day_check
    check (posts_per_day > 0),

  constraint campaigns_interval_check
    check (
      interval_minutes is null
      or interval_minutes > 0
    ),

  constraint campaigns_repeat_interval_check
    check (
      repeat_interval_days is null
      or repeat_interval_days > 0
    ),

  constraint campaigns_date_check
    check (
      end_date is null
      or end_date >= start_date
    )
);

create index if not exists campaigns_user_id_idx
  on public.campaigns(user_id);

create index if not exists campaigns_status_idx
  on public.campaigns(status);

create index if not exists campaigns_start_date_idx
  on public.campaigns(start_date);

drop trigger if exists campaigns_updated_at on public.campaigns;

create trigger campaigns_updated_at
before update on public.campaigns
for each row
execute function public.set_updated_at();

-- ============================================================================
-- CAMPAIGN ACCOUNTS
-- ============================================================================

create table if not exists public.campaign_accounts (
  id uuid primary key default gen_random_uuid(),

  campaign_id uuid not null
    references public.campaigns(id)
    on delete cascade,

  account_id uuid not null
    references public.social_accounts(id)
    on delete cascade,

  enabled boolean not null default true,

  created_at timestamptz not null default now(),

  unique(campaign_id, account_id)
);

create index if not exists campaign_accounts_campaign_idx
  on public.campaign_accounts(campaign_id);

create index if not exists campaign_accounts_account_idx
  on public.campaign_accounts(account_id);

-- ============================================================================
-- CAMPAIGN VIDEOS
-- ============================================================================

create table if not exists public.campaign_videos (
  id uuid primary key default gen_random_uuid(),

  campaign_id uuid not null
    references public.campaigns(id)
    on delete cascade,

  video_id uuid not null
    references public.videos(id)
    on delete cascade,

  position integer not null,

  enabled boolean not null default true,

  created_at timestamptz not null default now(),

  unique(campaign_id, video_id),

  unique(campaign_id, position)
);

create index if not exists campaign_videos_campaign_idx
  on public.campaign_videos(campaign_id);

create index if not exists campaign_videos_video_idx
  on public.campaign_videos(video_id);

-- ============================================================================
-- POSTS
-- ============================================================================

create table if not exists public.posts (
  id uuid primary key default gen_random_uuid(),

  user_id uuid not null
    references public.profiles(id)
    on delete cascade,

  campaign_id uuid
    references public.campaigns(id)
    on delete set null,

  account_id uuid not null
    references public.social_accounts(id)
    on delete cascade,

  video_id uuid not null
    references public.videos(id)
    on delete restrict,

  platform public.social_platform not null,

  status public.post_status not null default 'scheduled',

  scheduled_at timestamptz not null,

  published_at timestamptz,

  external_post_id text,

  external_post_url text,

  caption text,

  error_message text,

  retry_count integer not null default 0,

  max_retries integer not null default 3,

  cycle_number integer not null default 1,

  video_position integer,

  created_at timestamptz not null default now(),

  updated_at timestamptz not null default now(),

  constraint posts_retry_count_check
    check (retry_count >= 0),

  constraint posts_max_retries_check
    check (max_retries >= 0),

  constraint posts_cycle_check
    check (cycle_number > 0)
);

create index if not exists posts_user_id_idx
  on public.posts(user_id);

create index if not exists posts_campaign_id_idx
  on public.posts(campaign_id);

create index if not exists posts_account_id_idx
  on public.posts(account_id);

create index if not exists posts_video_id_idx
  on public.posts(video_id);

create index if not exists posts_status_idx
  on public.posts(status);

create index if not exists posts_scheduled_at_idx
  on public.posts(scheduled_at);

create index if not exists posts_queue_idx
  on public.posts(status, scheduled_at);

drop trigger if exists posts_updated_at on public.posts;

create trigger posts_updated_at
before update on public.posts
for each row
execute function public.set_updated_at();

-- ============================================================================
-- PUBLISHING JOBS
-- ============================================================================

create table if not exists public.publishing_jobs (
  id uuid primary key default gen_random_uuid(),

  post_id uuid not null
    references public.posts(id)
    on delete cascade,

  status public.job_status not null default 'pending',

  scheduled_for timestamptz not null,

  started_at timestamptz,

  completed_at timestamptz,

  locked_at timestamptz,

  worker_id text,

  attempts integer not null default 0,

  max_attempts integer not null default 3,

  last_error text,

  result jsonb,

  created_at timestamptz not null default now(),

  updated_at timestamptz not null default now(),

  constraint publishing_jobs_attempts_check
    check (attempts >= 0),

  constraint publishing_jobs_max_attempts_check
    check (max_attempts > 0)
);

create index if not exists publishing_jobs_status_idx
  on public.publishing_jobs(status);

create index if not exists publishing_jobs_scheduled_idx
  on public.publishing_jobs(scheduled_for);

create index if not exists publishing_jobs_queue_idx
  on public.publishing_jobs(status, scheduled_for);

create index if not exists publishing_jobs_post_idx
  on public.publishing_jobs(post_id);

drop trigger if exists publishing_jobs_updated_at
on public.publishing_jobs;

create trigger publishing_jobs_updated_at
before update on public.publishing_jobs
for each row
execute function public.set_updated_at();

-- ============================================================================
-- ANALYTICS
-- ============================================================================

create table if not exists public.analytics (
  id uuid primary key default gen_random_uuid(),

  user_id uuid not null
    references public.profiles(id)
    on delete cascade,

  account_id uuid
    references public.social_accounts(id)
    on delete cascade,

  post_id uuid
    references public.posts(id)
    on delete cascade,

  platform public.social_platform not null,

  external_post_id text,

  views bigint not null default 0,

  likes bigint not null default 0,

  comments bigint not null default 0,

  shares bigint not null default 0,

  saves bigint not null default 0,

  clicks bigint not null default 0,

  engagement_rate numeric(10,4) not null default 0,

  recorded_at timestamptz not null default now(),

  created_at timestamptz not null default now()
);

create index if not exists analytics_user_id_idx
  on public.analytics(user_id);

create index if not exists analytics_account_id_idx
  on public.analytics(account_id);

create index if not exists analytics_post_id_idx
  on public.analytics(post_id);

create index if not exists analytics_recorded_at_idx
  on public.analytics(recorded_at desc);

-- ============================================================================
-- LOGS
-- ============================================================================

create table if not exists public.logs (
  id uuid primary key default gen_random_uuid(),

  user_id uuid
    references public.profiles(id)
    on delete cascade,

  level text not null default 'info',

  service text not null,

  event text not null,

  message text,

  account_id uuid
    references public.social_accounts(id)
    on delete set null,

  campaign_id uuid
    references public.campaigns(id)
    on delete set null,

  post_id uuid
    references public.posts(id)
    on delete set null,

  job_id uuid
    references public.publishing_jobs(id)
    on delete set null,

  metadata jsonb not null default '{}'::jsonb,

  created_at timestamptz not null default now()
);

create index if not exists logs_user_id_idx
  on public.logs(user_id);

create index if not exists logs_level_idx
  on public.logs(level);

create index if not exists logs_service_idx
  on public.logs(service);

create index if not exists logs_created_at_idx
  on public.logs(created_at desc);

-- ============================================================================
-- NOTIFICATIONS
-- ============================================================================

create table if not exists public.notifications (
  id uuid primary key default gen_random_uuid(),

  user_id uuid not null
    references public.profiles(id)
    on delete cascade,

  title text not null,

  message text not null,

  type text not null default 'info',

  read boolean not null default false,

  metadata jsonb not null default '{}'::jsonb,

  created_at timestamptz not null default now()
);

create index if not exists notifications_user_id_idx
  on public.notifications(user_id);

create index if not exists notifications_unread_idx
  on public.notifications(user_id, read);

create index if not exists notifications_created_at_idx
  on public.notifications(created_at desc);

-- ============================================================================
-- ACCOUNT TRIGGERS / PROFILE CREATION
-- ============================================================================

create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
begin
  insert into public.profiles (
    id,
    email
  )
  values (
    new.id,
    new.email
  )
  on conflict (id) do nothing;

  return new;
end;
$$;

drop trigger if exists on_auth_user_created
on auth.users;

create trigger on_auth_user_created
after insert on auth.users
for each row
execute function public.handle_new_user();

-- ============================================================================
-- HELPER FUNCTIONS
-- ============================================================================

create or replace function public.get_next_video_position(
  p_campaign_id uuid
)
returns integer
language sql
stable
as $$
  select coalesce(max(position), -1) + 1
  from public.campaign_videos
  where campaign_id = p_campaign_id;
$$;

-- ============================================================================
-- COMMENTS
-- ============================================================================

comment on table public.profiles is
  'Application profiles linked to Supabase Auth users.';

comment on table public.social_accounts is
  'Connected Instagram, Facebook and TikTok accounts.';

comment on table public.videos is
  'Video content stored in Supabase Storage.';

comment on table public.campaigns is
  'Automated publishing campaigns and their scheduling configuration.';

comment on table public.campaign_accounts is
  'Accounts assigned to campaigns.';

comment on table public.campaign_videos is
  'Ordered videos assigned to campaigns.';

comment on table public.posts is
  'Individual scheduled or published social media posts.';

comment on table public.publishing_jobs is
  'Worker queue for publishing posts to social platforms.';

comment on table public.analytics is
  'Performance metrics collected from published posts.';

comment on table public.logs is
  'Application and worker logs.';

comment on table public.notifications is
  'Dashboard notifications for users.';
