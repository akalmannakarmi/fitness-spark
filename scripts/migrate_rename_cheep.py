import asyncio
import logging

from database import recipes_collection

logger = logging.getLogger(__name__)


async def migrate() -> None:
    """Rename the legacy ``cheep`` field to ``cheap`` on existing recipe docs.

    Manual migration - not run automatically. Safe to run multiple times.
    """
    cursor = recipes_collection.find({"cheep": {"$exists": True}})
    updated = 0

    async for doc in cursor:
        await recipes_collection.update_one(
            {"_id": doc["_id"]},
            {"$set": {"cheap": doc["cheep"]}, "$unset": {"cheep": ""}},
        )
        updated += 1

    logger.info("Migrated %s documents to use 'cheap'", updated)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(migrate())
