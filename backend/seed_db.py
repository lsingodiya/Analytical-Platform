import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from auth import MONGO_URI, DB_NAME, get_password_hash

async def seed_database():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]

    print("Seeding roles...")
    # Roles collection
    roles_data = [
        {"_id": "Admin", "permissions": ["all"]},
        {"_id": "Standard", "permissions": ["dashboard"]}
    ]
    for role in roles_data:
        await db.roles.replace_one({"_id": role["_id"]}, role, upsert=True)
    
    print("Seeding default users...")
    # Users collection
    users_data = [
        {
            "username": "admin", 
            "password": get_password_hash("admin123"), 
            "role": "Admin"
        },
        {
            "username": "user", 
            "password": get_password_hash("user123"), 
            "role": "Standard"
        },
    ]
    for user in users_data:
        await db.users.replace_one({"username": user["username"]}, user, upsert=True)

    print("Database seeded successfully!")
    print("\nDefault Credentials:")
    print("Admin: admin / admin123")
    print("Standard: user / user123")

if __name__ == "__main__":
    asyncio.run(seed_database())
