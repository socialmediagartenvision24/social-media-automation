-- ============================================================================
-- SOCIAL MEDIA AUTOMATION
-- Seed Data
-- ============================================================================
--
-- Dieses Seed-File erzeugt KEINE Fake-User und KEINE Social-Media-Accounts.
--
-- Warum?
--   - Auth-User werden über Supabase Auth angelegt.
--   - Social Accounts benötigen echte OAuth-Verbindungen.
--   - Access-/Refresh-Tokens gehören niemals in Seed-Daten.
--
-- Nach dem Anlegen eines echten Users können die Demo-Daten optional
-- mit der untenstehenden Funktion erzeugt werden.
-- ============================================================================


-- ============================================================================
-- DEMO DATA FUNCTION
-- ============================================================================
--
-- Verwendung:
--
-- select public.create_demo_data('DEINE-USER-UUID');
--
-- Die UUID muss zu einem existierenden auth.users / profiles Datensatz gehören.
-- ============================================================================

create or replace function public.create_demo_data(
  p_user_id uuid
)
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare
  v_campaign_id uuid;

  v_video_1 uuid;
  v_video_2 uuid;
  v_video_3 uuid;

  v_account_id uuid;

  v_result jsonb;
begin

  -- --------------------------------------------------------------------------
  -- Check user
  -- --------------------------------------------------------------------------

  if not exists (
    select 1
    from public.profiles
    where id = p_user_id
  ) then
    raise exception 'Profile für User % existiert nicht.', p_user_id;
  end if;


  -- --------------------------------------------------------------------------
  -- Demo videos
  -- --------------------------------------------------------------------------

  insert into public.videos (
    user_id,
    name,
    description,
    storage_path,
    mime_type,
    file_size_bytes,
    duration_seconds,
    status
  )
  values (
    p_user_id,
    'Demo Video 01',
    'Demo-Video für die Automation.',
    'demo/' || p_user_id::text || '/demo-video-01.mp4',
    'video/mp4',
    0,
    15,
    'ready'
  )
  returning id into v_video_1;


  insert into public.videos (
    user_id,
    name,
    description,
    storage_path,
    mime_type,
    file_size_bytes,
    duration_seconds,
    status
  )
  values (
    p_user_id,
    'Demo Video 02',
    'Demo-Video für die Automation.',
    'demo/' || p_user_id::text || '/demo-video-02.mp4',
    'video/mp4',
    0,
    20,
    'ready'
  )
  returning id into v_video_2;


  insert into public.videos (
    user_id,
    name,
    description,
    storage_path,
    mime_type,
    file_size_bytes,
    duration_seconds,
    status
  )
  values (
    p_user_id,
    'Demo Video 03',
    'Demo-Video für die Automation.',
    'demo/' || p_user_id::text || '/demo-video-03.mp4',
    'video/mp4',
    0,
    30,
    'ready'
  )
  returning id into v_video_3;


  -- --------------------------------------------------------------------------
  -- Demo campaign
  -- --------------------------------------------------------------------------

  insert into public.campaigns (
    user_id,
    name,
    description,
    status,
    timezone,
    start_date,
    posts_per_day,
    schedule_mode,
    posting_times,
    repeat_enabled,
    repeat_interval_days
  )
  values (
    p_user_id,
    'Demo Kampagne',
    'Beispielkampagne für das Dashboard.',
    'draft',
    'Europe/Berlin',
    current_date,
    3,
    'fixed',
    '[
      "09:00",
      "13:00",
      "18:00"
    ]'::jsonb,
    true,
    30
  )
  returning id into v_campaign_id;


  -- --------------------------------------------------------------------------
  -- Demo campaign videos
  -- --------------------------------------------------------------------------

  insert into public.campaign_videos (
    campaign_id,
    video_id,
    position,
    enabled
  )
  values
    (
      v_campaign_id,
      v_video_1,
      1,
      true
    ),
    (
      v_campaign_id,
      v_video_2,
      2,
      true
    ),
    (
      v_campaign_id,
      v_video_3,
      3,
      true
    );


  -- --------------------------------------------------------------------------
  -- Optional demo account
  -- --------------------------------------------------------------------------
  --
  -- Dieser Account ist absichtlich NICHT als verbunden markiert.
  -- Es werden keine Tokens gespeichert.
  --

  insert into public.social_accounts (
    user_id,
    platform,
    name,
    username,
    platform_account_id,
    status,
    timezone
  )
  values (
    p_user_id,
    'instagram',
    'Demo Instagram',
    'demo_account',
    'demo-' || p_user_id::text,
    'disconnected',
    'Europe/Berlin'
  )
  on conflict (
    user_id,
    platform,
    platform_account_id
  )
  do nothing
  returning id into v_account_id;


  -- --------------------------------------------------------------------------
  -- Connect demo account to campaign
  -- --------------------------------------------------------------------------

  if v_account_id is not null then

    insert into public.campaign_accounts (
      campaign_id,
      account_id,
      enabled
    )
    values (
      v_campaign_id,
      v_account_id,
      true
    )
    on conflict (
      campaign_id,
      account_id
    )
    do nothing;

  end if;


  -- --------------------------------------------------------------------------
  -- Result
  -- --------------------------------------------------------------------------

  v_result := jsonb_build_object(
    'success', true,
    'campaign_id', v_campaign_id,
    'video_ids', jsonb_build_array(
      v_video_1,
      v_video_2,
      v_video_3
    ),
    'account_id', v_account_id
  );

  return v_result;

end;
$$;


-- ============================================================================
-- SECURITY
-- ============================================================================

revoke all
on function public.create_demo_data(uuid)
from public;


-- ============================================================================
-- IMPORTANT
-- ============================================================================
--
-- Die Funktion ist absichtlich nicht automatisch ausführbar.
--
-- Nach dem Erstellen eines Users kann sie serverseitig aufgerufen werden.
--
-- Beispiel:
--
-- select public.create_demo_data(
--   '00000000-0000-0000-0000-000000000000'
-- );
--
-- Ersetze die UUID durch die echte ID aus auth.users.
--
-- ============================================================================


-- ============================================================================
-- OPTIONAL: DEMO DATA DOCUMENTATION
-- ============================================================================

comment on function public.create_demo_data(uuid)
is
'Creates safe demo campaign data for an existing application user. No real OAuth credentials are created.';
