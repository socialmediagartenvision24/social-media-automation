-- ============================================================================
-- SOCIAL MEDIA AUTOMATION
-- Migration: 003_storage.sql
-- Supabase Storage
-- ============================================================================

-- ============================================================================
-- VIDEO BUCKET
-- ============================================================================

insert into storage.buckets (
  id,
  name,
  public
)
values (
  'videos',
  'videos',
  false
)
on conflict (id)
do update set
  public = false;

-- ============================================================================
-- STORAGE POLICIES
-- ============================================================================
--
-- Dateien werden nach diesem Schema gespeichert:
--
-- videos/
--   USER_ID/
--     VIDEO_ID/
--       original.mp4
--       thumbnail.jpg
--
-- Dadurch kann jeder User nur seinen eigenen Ordner verwalten.
-- ============================================================================


-- ============================================================================
-- SELECT
-- ============================================================================

drop policy if exists "videos_storage_select_own"
on storage.objects;

create policy "videos_storage_select_own"
on storage.objects
for select
to authenticated
using (
  bucket_id = 'videos'
  and (
    (storage.foldername(name))[1] = auth.uid()::text
  )
);


-- ============================================================================
-- INSERT
-- ============================================================================

drop policy if exists "videos_storage_insert_own"
on storage.objects;

create policy "videos_storage_insert_own"
on storage.objects
for insert
to authenticated
with check (
  bucket_id = 'videos'
  and (
    (storage.foldername(name))[1] = auth.uid()::text
  )
);


-- ============================================================================
-- UPDATE
-- ============================================================================

drop policy if exists "videos_storage_update_own"
on storage.objects;

create policy "videos_storage_update_own"
on storage.objects
for update
to authenticated
using (
  bucket_id = 'videos'
  and (
    (storage.foldername(name))[1] = auth.uid()::text
  )
)
with check (
  bucket_id = 'videos'
  and (
    (storage.foldername(name))[1] = auth.uid()::text
  )
);


-- ============================================================================
-- DELETE
-- ============================================================================

drop policy if exists "videos_storage_delete_own"
on storage.objects;

create policy "videos_storage_delete_own"
on storage.objects
for delete
to authenticated
using (
  bucket_id = 'videos'
  and (
    (storage.foldername(name))[1] = auth.uid()::text
  )
);


-- ============================================================================
-- THUMBNAIL SUPPORT
-- ============================================================================
--
-- Thumbnails liegen ebenfalls im videos Bucket:
--
-- videos/
--   USER_ID/
--     VIDEO_ID/
--       original.mp4
--       thumbnail.jpg
--
-- Der Worker kann später Thumbnails erzeugen und serverseitig hochladen.
-- ============================================================================


-- ============================================================================
-- STORAGE METADATA INDEX
-- ============================================================================

create index if not exists storage_objects_videos_bucket_name_idx
on storage.objects(bucket_id, name)
where bucket_id = 'videos';
