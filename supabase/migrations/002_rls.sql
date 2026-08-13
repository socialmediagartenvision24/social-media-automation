-- ============================================================================
-- SOCIAL MEDIA AUTOMATION
-- Migration: 002_rls.sql
-- Row Level Security
-- ============================================================================
--
-- SECURITY MODEL
--
-- 1. Normal users can only access their own data.
-- 2. OAuth credentials are NEVER readable by authenticated users.
-- 3. Publishing workers use the Supabase service role server-side.
-- 4. Service-role credentials must NEVER reach the frontend.
--
-- ============================================================================


-- ============================================================================
-- ENABLE RLS
-- ============================================================================

alter table public.profiles enable row level security;
alter table public.social_accounts enable row level security;
alter table public.videos enable row level security;
alter table public.campaigns enable row level security;
alter table public.campaign_accounts enable row level security;
alter table public.campaign_videos enable row level security;
alter table public.posts enable row level security;
alter table public.publishing_jobs enable row level security;
alter table public.analytics enable row level security;
alter table public.logs enable row level security;
alter table public.notifications enable row level security;


-- ============================================================================
-- PROFILES
-- ============================================================================

drop policy if exists "profiles_select_own"
on public.profiles;

create policy "profiles_select_own"
on public.profiles
for select
to authenticated
using (
    id = auth.uid()
);


drop policy if exists "profiles_insert_own"
on public.profiles;

create policy "profiles_insert_own"
on public.profiles
for insert
to authenticated
with check (
    id = auth.uid()
);


drop policy if exists "profiles_update_own"
on public.profiles;

create policy "profiles_update_own"
on public.profiles
for update
to authenticated
using (
    id = auth.uid()
)
with check (
    id = auth.uid()
);


-- ============================================================================
-- SOCIAL ACCOUNTS
-- ============================================================================

drop policy if exists "social_accounts_select_own"
on public.social_accounts;

create policy "social_accounts_select_own"
on public.social_accounts
for select
to authenticated
using (
    user_id = auth.uid()
);


drop policy if exists "social_accounts_insert_own"
on public.social_accounts;

create policy "social_accounts_insert_own"
on public.social_accounts
for insert
to authenticated
with check (
    user_id = auth.uid()
);


drop policy if exists "social_accounts_update_own"
on public.social_accounts;

create policy "social_accounts_update_own"
on public.social_accounts
for update
to authenticated
using (
    user_id = auth.uid()
)
with check (
    user_id = auth.uid()
);


drop policy if exists "social_accounts_delete_own"
on public.social_accounts;

create policy "social_accounts_delete_own"
on public.social_accounts
for delete
to authenticated
using (
    user_id = auth.uid()
);


-- ============================================================================
-- SOCIAL ACCOUNT TOKEN PROTECTION
-- ============================================================================
--
-- RLS protects ROWS.
--
-- OAuth credentials require COLUMN protection as well.
--
-- The frontend must never be able to SELECT:
--
--   access_token
--   refresh_token
--   token_expires_at
--   refresh_token_expires_at
--
-- The backend/service-role can still access these values.
--
-- ============================================================================

revoke select (
    access_token,
    refresh_token,
    token_expires_at,
    refresh_token_expires_at
)
on public.social_accounts
from anon;

revoke select (
    access_token,
    refresh_token,
    token_expires_at,
    refresh_token_expires_at
)
on public.social_accounts
from authenticated;


-- ============================================================================
-- VIDEOS
-- ============================================================================

drop policy if exists "videos_select_own"
on public.videos;

create policy "videos_select_own"
on public.videos
for select
to authenticated
using (
    user_id = auth.uid()
);


drop policy if exists "videos_insert_own"
on public.videos;

create policy "videos_insert_own"
on public.videos
for insert
to authenticated
with check (
    user_id = auth.uid()
);


drop policy if exists "videos_update_own"
on public.videos;

create policy "videos_update_own"
on public.videos
for update
to authenticated
using (
    user_id = auth.uid()
)
with check (
    user_id = auth.uid()
);


drop policy if exists "videos_delete_own"
on public.videos;

create policy "videos_delete_own"
on public.videos
for delete
to authenticated
using (
    user_id = auth.uid()
);


-- ============================================================================
-- CAMPAIGNS
-- ============================================================================

drop policy if exists "campaigns_select_own"
on public.campaigns;

create policy "campaigns_select_own"
on public.campaigns
for select
to authenticated
using (
    user_id = auth.uid()
);


drop policy if exists "campaigns_insert_own"
on public.campaigns;

create policy "campaigns_insert_own"
on public.campaigns
for insert
to authenticated
with check (
    user_id = auth.uid()
);


drop policy if exists "campaigns_update_own"
on public.campaigns;

create policy "campaigns_update_own"
on public.campaigns
for update
to authenticated
using (
    user_id = auth.uid()
)
with check (
    user_id = auth.uid()
);


drop policy if exists "campaigns_delete_own"
on public.campaigns;

create policy "campaigns_delete_own"
on public.campaigns
for delete
to authenticated
using (
    user_id = auth.uid()
);


-- ============================================================================
-- CAMPAIGN ACCOUNTS
-- ============================================================================

drop policy if exists "campaign_accounts_select_own"
on public.campaign_accounts;

create policy "campaign_accounts_select_own"
on public.campaign_accounts
for select
to authenticated
using (
    exists (
        select 1
        from public.campaigns c
        where c.id = campaign_accounts.campaign_id
          and c.user_id = auth.uid()
    )
);


drop policy if exists "campaign_accounts_insert_own"
on public.campaign_accounts;

create policy "campaign_accounts_insert_own"
on public.campaign_accounts
for insert
to authenticated
with check (
    exists (
        select 1
        from public.campaigns c
        where c.id = campaign_accounts.campaign_id
          and c.user_id = auth.uid()
    )
    and exists (
        select 1
        from public.social_accounts a
        where a.id = campaign_accounts.account_id
          and a.user_id = auth.uid()
    )
);


drop policy if exists "campaign_accounts_update_own"
on public.campaign_accounts;

create policy "campaign_accounts_update_own"
on public.campaign_accounts
for update
to authenticated
using (
    exists (
        select 1
        from public.campaigns c
        where c.id = campaign_accounts.campaign_id
          and c.user_id = auth.uid()
    )
)
with check (
    exists (
        select 1
        from public.campaigns c
        where c.id = campaign_accounts.campaign_id
          and c.user_id = auth.uid()
    )
    and exists (
        select 1
        from public.social_accounts a
        where a.id = campaign_accounts.account_id
          and a.user_id = auth.uid()
    )
);


drop policy if exists "campaign_accounts_delete_own"
on public.campaign_accounts;

create policy "campaign_accounts_delete_own"
on public.campaign_accounts
for delete
to authenticated
using (
    exists (
        select 1
        from public.campaigns c
        where c.id = campaign_accounts.campaign_id
          and c.user_id = auth.uid()
    )
);


-- ============================================================================
-- CAMPAIGN VIDEOS
-- ============================================================================

drop policy if exists "campaign_videos_select_own"
on public.campaign_videos;

create policy "campaign_videos_select_own"
on public.campaign_videos
for select
to authenticated
using (
    exists (
        select 1
        from public.campaigns c
        where c.id = campaign_videos.campaign_id
          and c.user_id = auth.uid()
    )
);


drop policy if exists "campaign_videos_insert_own"
on public.campaign_videos;

create policy "campaign_videos_insert_own"
on public.campaign_videos
for insert
to authenticated
with check (
    exists (
        select 1
        from public.campaigns c
        where c.id = campaign_videos.campaign_id
          and c.user_id = auth.uid()
    )
    and exists (
        select 1
        from public.videos v
        where v.id = campaign_videos.video_id
          and v.user_id = auth.uid()
    )
);


drop policy if exists "campaign_videos_update_own"
on public.campaign_videos;

create policy "campaign_videos_update_own"
on public.campaign_videos
for update
to authenticated
using (
    exists (
        select 1
        from public.campaigns c
        where c.id = campaign_videos.campaign_id
          and c.user_id = auth.uid()
    )
)
with check (
    exists (
        select 1
        from public.campaigns c
        where c.id = campaign_videos.campaign_id
          and c.user_id = auth.uid()
    )
    and exists (
        select 1
        from public.videos v
        where v.id = campaign_videos.video_id
          and v.user_id = auth.uid()
    )
);


drop policy if exists "campaign_videos_delete_own"
on public.campaign_videos;

create policy "campaign_videos_delete_own"
on public.campaign_videos
for delete
to authenticated
using (
    exists (
        select 1
        from public.campaigns c
        where c.id = campaign_videos.campaign_id
          and c.user_id = auth.uid()
    )
);


-- ============================================================================
-- POSTS
-- ============================================================================

drop policy if exists "posts_select_own"
on public.posts;

create policy "posts_select_own"
on public.posts
for select
to authenticated
using (
    user_id = auth.uid()
);


drop policy if exists "posts_insert_own"
on public.posts;

create policy "posts_insert_own"
on public.posts
for insert
to authenticated
with check (
    user_id = auth.uid()
);


drop policy if exists "posts_update_own"
on public.posts;

create policy "posts_update_own"
on public.posts
for update
to authenticated
using (
    user_id = auth.uid()
)
with check (
    user_id = auth.uid()
);


drop policy if exists "posts_delete_own"
on public.posts;

create policy "posts_delete_own"
on public.posts
for delete
to authenticated
using (
    user_id = auth.uid()
);


-- ============================================================================
-- PUBLISHING JOBS
-- ============================================================================
--
-- Users can see jobs belonging to their own posts.
--
-- Creation/update/deletion is primarily a backend responsibility.
-- This prevents users from manipulating the publishing worker directly.
--
-- ============================================================================

drop policy if exists "publishing_jobs_select_own"
on public.publishing_jobs;

create policy "publishing_jobs_select_own"
on public.publishing_jobs
for select
to authenticated
using (
    exists (
        select 1
        from public.posts p
        where p.id = publishing_jobs.post_id
          and p.user_id = auth.uid()
    )
);


-- ============================================================================
-- ANALYTICS
-- ============================================================================
--
-- Analytics are generated by the backend/platform integrations.
-- Users only need read access.
--
-- ============================================================================

drop policy if exists "analytics_select_own"
on public.analytics;

create policy "analytics_select_own"
on public.analytics
for select
to authenticated
using (
    user_id = auth.uid()
);


-- ============================================================================
-- LOGS
-- ============================================================================
--
-- Logs are generated by the backend.
-- Users can only read their own logs.
--
-- ============================================================================

drop policy if exists "logs_select_own"
on public.logs;

create policy "logs_select_own"
on public.logs
for select
to authenticated
using (
    user_id = auth.uid()
);


-- ============================================================================
-- NOTIFICATIONS
-- ============================================================================
--
-- Notifications are generated by the backend.
-- Users can read/update/delete their own notifications.
--
-- ============================================================================

drop policy if exists "notifications_select_own"
on public.notifications;

create policy "notifications_select_own"
on public.notifications
for select
to authenticated
using (
    user_id = auth.uid()
);


drop policy if exists "notifications_update_own"
on public.notifications;

create policy "notifications_update_own"
on public.notifications
for update
to authenticated
using (
    user_id = auth.uid()
)
with check (
    user_id = auth.uid()
);


drop policy if exists "notifications_delete_own"
on public.notifications;

create policy "notifications_delete_own"
on public.notifications
for delete
to authenticated
using (
    user_id = auth.uid()
);


-- ============================================================================
-- ANONYMOUS ACCESS
-- ============================================================================
--
-- No application data is intentionally exposed to anonymous users.
--
-- ============================================================================

revoke all
on public.profiles
from anon;

revoke all
on public.social_accounts
from anon;

revoke all
on public.videos
from anon;

revoke all
on public.campaigns
from anon;

revoke all
on public.campaign_accounts
from anon;

revoke all
on public.campaign_videos
from anon;

revoke all
on public.posts
from anon;

revoke all
on public.publishing_jobs
from anon;

revoke all
on public.analytics
from anon;

revoke all
on public.logs
from anon;

revoke all
on public.notifications
from anon;


-- ============================================================================
-- SERVICE ROLE
-- ============================================================================
--
-- Supabase's service_role bypasses RLS.
--
-- It is used ONLY by the trusted backend/worker.
--
-- NEVER expose the service-role key to:
--
--   - Next.js client code
--   - browser JavaScript
--   - NEXT_PUBLIC_* variables
--   - GitHub
--   - public Docker images
--   - API responses
--
-- ============================================================================


-- ============================================================================
-- END
-- ============================================================================
