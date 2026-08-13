from datetime import datetime, timedelta
from typing import Iterable


def generate_schedule(
    start: datetime,
    count: int,
    interval_minutes: int,
) -> list[datetime]:
    """
    Generate a simple sequence of scheduled timestamps.

    The production scheduler will additionally handle:
    - campaign timezone
    - posting times
    - account-specific schedules
    - repeat cycles
    - enabled/disabled videos
    - platform restrictions
    """

    if count <= 0:
        return []

    if interval_minutes <= 0:
        raise ValueError("interval_minutes muss größer als 0 sein.")

    return [
        start + timedelta(minutes=index * interval_minutes)
        for index in range(count)
    ]
