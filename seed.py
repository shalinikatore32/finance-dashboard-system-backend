import asyncio
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
import sys

# Ensure app modules can be imported
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.security import get_password_hash
from app.core.config import settings

async def seed_data():
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.DATABASE_NAME]

    print("Clearing existing data...")
    await db.users.delete_many({})
    await db.transactions.delete_many({})

    print("Creating users...")
    users = [
        {
            "name": "Admin User",
            "email": "admin@example.com",
            "hashed_password": get_password_hash("password123"),
            "role": "Admin",
            "is_active": True,
            "created_at": datetime.utcnow()
        },
        {
            "name": "Analyst User",
            "email": "analyst@example.com",
            "hashed_password": get_password_hash("password123"),
            "role": "Analyst",
            "is_active": True,
            "created_at": datetime.utcnow()
        },
        {
            "name": "Viewer User",
            "email": "viewer@example.com",
            "hashed_password": get_password_hash("password123"),
            "role": "Viewer",
            "is_active": True,
            "created_at": datetime.utcnow()
        }
    ]
    
    user_results = await db.users.insert_many(users)
    admin_id = user_results.inserted_ids[0]

    print("Creating transactions...")
    today = datetime.utcnow()
    transactions = [
        {
            "amount": 5000.0,
            "type": "income",
            "category": "Salary",
            "date": today - timedelta(days=20),
            "notes": "Monthly salary",
            "created_by": str(admin_id),
            "created_at": datetime.utcnow(),
            "is_deleted": False
        },
        {
            "amount": 1200.0,
            "type": "expense",
            "category": "Rent",
            "date": today - timedelta(days=15),
            "notes": "Office rent",
            "created_by": str(admin_id),
            "created_at": datetime.utcnow(),
            "is_deleted": False
        },
        {
            "amount": 150.0,
            "type": "expense",
            "category": "Utilities",
            "date": today - timedelta(days=5),
            "notes": "Internet bill",
            "created_by": str(admin_id),
            "created_at": datetime.utcnow(),
            "is_deleted": False
        }
    ]
    
    await db.transactions.insert_many(transactions)

    client.close()
    print("Database seeded successfully!")
    print("Login credentials:")
    print("Admin: admin@example.com / password123")
    print("Analyst: analyst@example.com / password123")
    print("Viewer: viewer@example.com / password123")

if __name__ == "__main__":
    asyncio.run(seed_data())
