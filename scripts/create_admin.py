import asyncio
import getpass
import logging

from database import users_collection
from security import hash_password

logger = logging.getLogger(__name__)


async def create_admin() -> str | None:
    """Create an admin user in the database."""
    username = input("Enter Username: ")
    email = input("Enter Email: ")

    password = getpass.getpass("Enter Password: ")
    conf_password = getpass.getpass("Confirm Password: ")

    if password != conf_password:
        logger.error("Passwords do not match!")
        return None

    result = await users_collection.insert_one(
        {
            "username": username,
            "email": email,
            "password": hash_password(password),
            "groups": ["admin"],
        }
    )

    logger.info("Created Admin successfully!")
    return str(result.inserted_id)


async def main() -> None:
    """CLI Tool for Fitness Spark."""
    while True:
        print("\nWelcome To Fitness Spark Tools!")
        print("0) Exit")
        print("1) Create Admin")

        choice = input("Choice: ").strip()

        if choice == "0" or choice == "":
            logger.info("Exiting... Goodbye!")
            break
        if choice == "1":
            await create_admin()
        else:
            logger.error("Invalid choice! Please try again.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
