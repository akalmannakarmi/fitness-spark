import asyncio
import getpass
from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL, DATABASE_NAME
from passlib.context import CryptContext

# Database Connection
client = AsyncIOMotorClient(MONGO_URL)
database = client[DATABASE_NAME]
users_collection = database["users"]

# Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

async def create_admin():
    """Creates an admin user in the database."""
    username = input("Enter Username: ")
    email = input("Enter Email: ")
    
    password = getpass.getpass("Enter Password: ")
    conf_password = getpass.getpass("Confirm Password: ")

    if password != conf_password:
        print("❌ Passwords do not match!")
        return

    result = await users_collection.insert_one({
        "username": username,
        "email": email,
        "password": hash_password(password),
        "groups": ["admin"]
    })
    
    print("✅ Created Admin successfully!")
    return str(result.inserted_id)

async def main():
    """CLI Tool for Fitness Spark"""
    while True:
        print("\nWelcome To Fitness Spark Tools!")
        print("0) Exit")
        print("1) Create Admin")

        choice = input("Choice: ").strip()

        if choice == "0" or choice == "":
            print("👋 Exiting... Goodbye!")
            break
        elif choice == "1":
            await create_admin()
        else:
            print("❌ Invalid choice! Please try again.")

if __name__ == "__main__":
    asyncio.run(main())
