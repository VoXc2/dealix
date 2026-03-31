import asyncio
from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

async def seed():
    db = SessionLocal()
    # 1. إنشاء مدير النظام
    admin = db.query(User).filter(User.email == "admin@dealix.sa").first()
    if not admin:
        admin = User(
            email="admin@dealix.sa",
            hashed_password=get_password_hash("admin123"),
            full_name="Engineer Admin",
            is_superuser=True
        )
        db.add(admin)
        db.commit()
        print("✅ Admin created: admin@dealix.sa / admin123")
    db.close()

if __name__ == "__main__":
    asyncio.run(seed())