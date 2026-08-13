from __future__ import annotations

from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

from fastapi import HTTPException, status

from app.services.supabase import get_supabase_admin


def _parse_time(value: str) -> time:
    """
    Parse HH:MM into a Python time object.
    """

    try:
        hour, minute = value.split(":")

        hour_int = int(hour)
        minute_int = int(minute)

        if not 0 <= hour_int <= 23:
            raise ValueError

        if not 0 <= minute_int <= 59:
            raise ValueError

        return time(
            hour=hour_int,
            minute=minute_int,
        )

    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ungültige Uhrzeit: {value}. Erwartet wird HH:MM.",
        )


def _generate_daily_times(
    posting_times: list[str],
    start_date: date,
    end_date: date,
    timezone_name: str,
) -> list[datetime]:
    """
    Generate timestamps for fixed daily posting times.
    """

    try:
        timezone = ZoneInfo(timezone_name)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ungültige Zeitzone: {timezone_name}",
        )

    parsed_times = [
        _parse_time(value)
        for value in posting_times
    ]

    timestamps: list[datetime] = []

    current_date = start_date

    while current_date <= end_date:
        for posting_time in parsed_times:
            timestamps.append(
                datetime.combine(
                    current_date,
                    posting_time,
                    tzinfo=timezone,
                )
            )

        current_date += timedelta(days=1)

    timestamps.sort()

    return timestamps


def _generate_interval_times(
    start_datetime: datetime,
    end_datetime: datetime,
    interval_minutes: int,
) -> list[datetime]:
    """
    Generate timestamps based on an interval.
    """

    if interval_minutes <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="interval_minutes muss größer als 0 sein.",
        )

    timestamps: list[datetime] = []

    current = start_datetime

    while current <= end_datetime:
        timestamps.append(current)
        current += timedelta(minutes=interval_minutes)

    return timestamps


def _cycle_videos(
    videos: list[dict],
    count: int,
) -> list[dict]:
    """
    Repeat the configured videos until the required number
    of posts has been generated.

    Example:

        [1, 2, 3]
        count = 8

        -> [1, 2, 3, 1, 2, 3, 1, 2]
    """

    if not videos:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Die Kampagne enthält keine Videos.",
        )

    return [
        videos[index % len(videos)]
        for index in range(count)
    ]


async def generate_campaign_posts(
    campaign_id: str,
    user_id: str,
) -> list[dict]:
    """
    Generate all posts for a campaign.

    The campaign configuration determines:
      - accounts
      - videos
      - dates
      - posting times
      - interval
      - repeat behavior

    Each account receives the generated schedule.
    """

    supabase = get_supabase_admin()

    # ----------------------------------------------------------------------
    # Campaign
    # ----------------------------------------------------------------------

    campaign_result = (
        supabase
        .table("campaigns")
        .select("*")
        .eq("id", campaign_id)
        .eq("user_id", user_id)
        .maybe_single()
        .execute()
    )

    campaign = campaign_result.data

    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kampagne nicht gefunden.",
        )

    # ----------------------------------------------------------------------
    # Campaign accounts
    # ----------------------------------------------------------------------

    account_links_result = (
        supabase
        .table("campaign_accounts")
        .select(
            """
            account_id,
            enabled
            """
        )
        .eq("campaign_id", campaign_id)
        .execute()
    )

    account_links = [
        item
        for item in (account_links_result.data or [])
        if item.get("enabled", True)
    ]

    if not account_links:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Die Kampagne enthält keine aktiven Accounts.",
        )

    account_ids = [
        item["account_id"]
        for item in account_links
    ]

    # ----------------------------------------------------------------------
    # Accounts belonging to current user
    # ----------------------------------------------------------------------

    accounts_result = (
        supabase
        .table("social_accounts")
        .select(
            """
            id,
            platform,
            status,
            timezone
            """
        )
        .in_("id", account_ids)
        .eq("user_id", user_id)
        .execute()
    )

    accounts = accounts_result.data or []

    if not accounts:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Keine gültigen Social Accounts gefunden.",
        )

    # ----------------------------------------------------------------------
    # Campaign videos
    # ----------------------------------------------------------------------

    video_links_result = (
        supabase
        .table("campaign_videos")
        .select(
            """
            video_id,
            position,
            enabled
            """
        )
        .eq("campaign_id", campaign_id)
        .execute()
    )

    video_links = [
        item
        for item in (video_links_result.data or [])
        if item.get("enabled", True)
    ]

    video_links.sort(
        key=lambda item: item.get("position", 0)
    )

    video_ids = [
        item["video_id"]
        for item in video_links
    ]

    if not video_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Die Kampagne enthält keine aktiven Videos.",
        )

    # ----------------------------------------------------------------------
    # Videos belonging to current user
    # ----------------------------------------------------------------------

    videos_result = (
        supabase
        .table("videos")
        .select(
            """
            id,
            name,
            status
            """
        )
        .in_("id", video_ids)
        .eq("user_id", user_id)
        .execute()
    )

    videos_by_id = {
        video["id"]: video
        for video in (videos_result.data or [])
    }

    videos = [
        videos_by_id[video_id]
        for video_id in video_ids
        if video_id in videos_by_id
    ]

    if not videos:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Keine gültigen Videos gefunden.",
        )

    # ----------------------------------------------------------------------
    # Dates
    # ----------------------------------------------------------------------

    start_date = date.fromisoformat(
        str(campaign["start_date"])
    )

    end_date_value = campaign.get("end_date")

    if end_date_value:
        end_date = date.fromisoformat(
            str(end_date_value)
        )
    else:
        # If no end date exists, create one cycle.
        repeat_days = campaign.get(
            "repeat_interval_days"
        ) or 30

        end_date = start_date + timedelta(
            days=repeat_days - 1
        )

    timezone_name = (
        campaign.get("timezone")
        or "Europe/Berlin"
    )

    # ----------------------------------------------------------------------
    # Generate timestamps
    # ----------------------------------------------------------------------

    schedule_mode = campaign.get(
        "schedule_mode"
    ) or "fixed"

    if schedule_mode == "fixed":

        posting_times = campaign.get(
            "posting_times"
        ) or []

        if isinstance(posting_times, str):
            import json

            posting_times = json.loads(
                posting_times
            )

        if not posting_times:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Keine Posting-Zeiten konfiguriert.",
            )

        timestamps = _generate_daily_times(
            posting_times=posting_times,
            start_date=start_date,
            end_date=end_date,
            timezone_name=timezone_name,
        )

    else:

        interval_minutes = campaign.get(
            "interval_minutes"
        )

        if not interval_minutes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="interval_minutes fehlt.",
            )

        timezone = ZoneInfo(
            timezone_name
        )

        start_datetime = datetime.combine(
            start_date,
            time(9, 0),
            tzinfo=timezone,
        )

        end_datetime = datetime.combine(
            end_date,
            time(23, 59),
            tzinfo=timezone,
        )

        timestamps = _generate_interval_times(
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            interval_minutes=interval_minutes,
        )

    if not timestamps:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Es konnten keine Posting-Zeitpunkte erzeugt werden.",
        )

    # ----------------------------------------------------------------------
    # Cycle videos
    # ----------------------------------------------------------------------

    scheduled_videos = _cycle_videos(
        videos=videos,
        count=len(timestamps),
    )

    # ----------------------------------------------------------------------
    # Existing posts
    # ----------------------------------------------------------------------

    existing_result = (
        supabase
        .table("posts")
        .select(
            """
            account_id,
            video_id,
            scheduled_at
            """
        )
        .eq("user_id", user_id)
        .eq("campaign_id", campaign_id)
        .execute()
    )

    existing = {
        (
            item["account_id"],
            item["video_id"],
            item["scheduled_at"],
        )
        for item in (existing_result.data or [])
    }

    # ----------------------------------------------------------------------
    # Generate posts
    # ----------------------------------------------------------------------

    posts_to_insert: list[dict] = []

    for account in accounts:

        platform = account["platform"]

        for index, timestamp in enumerate(
            timestamps
        ):

            video = scheduled_videos[index]

            scheduled_iso = timestamp.isoformat()

            key = (
                account["id"],
                video["id"],
                scheduled_iso,
            )

            if key in existing:
                continue

            posts_to_insert.append(
                {
                    "user_id": user_id,
                    "campaign_id": campaign_id,
                    "account_id": account["id"],
                    "video_id": video["id"],
                    "platform": platform,
                    "status": "scheduled",
                    "scheduled_at": scheduled_iso,
                    "retry_count": 0,
                    "max_retries": 3,
                    "cycle_number": (
                        index // len(videos)
                    ) + 1,
                }
            )

    # ----------------------------------------------------------------------
    # Insert
    # ----------------------------------------------------------------------

    if not posts_to_insert:
        return []

    result = (
        supabase
        .table("posts")
        .insert(posts_to_insert)
        .execute()
    )

    return result.data or []
