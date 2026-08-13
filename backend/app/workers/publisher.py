from __future__ import annotations

import asyncio
import logging

from app.services.queue_service import enqueue_due_posts


logger = logging.getLogger(__name__)


class PublisherWorker:
    """
    Background worker responsible for moving due scheduled
    posts into the publishing queue.

    Platform publishing is delegated to platform adapters.
    """

    def __init__(
        self,
        interval_seconds: int = 30,
    ):
        self.interval_seconds = interval_seconds
        self.running = False

    async def process_once(self) -> None:
        try:
            queued = await enqueue_due_posts(
                limit=100,
            )

            if queued:
                logger.info(
                    "Queued %s posts for publishing.",
                    len(queued),
                )

        except Exception:
            logger.exception(
                "Error while processing publishing queue."
            )

    async def run(self) -> None:
        self.running = True

        logger.info(
            "Publisher worker started."
        )

        while self.running:

            await self.process_once()

            await asyncio.sleep(
                self.interval_seconds
            )

    def stop(self) -> None:
        self.running = False

        logger.info(
            "Publisher worker stopped."
        )
