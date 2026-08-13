import asyncio
import logging

from app.workers.publisher import PublisherWorker


logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    ),
)


async def main():
    worker = PublisherWorker(
        interval_seconds=30,
    )

    try:
        await worker.run()

    except KeyboardInterrupt:
        worker.stop()


if __name__ == "__main__":
    asyncio.run(main())
