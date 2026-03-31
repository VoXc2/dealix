from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .core.database import engine, Base, AsyncSessionLocal
from .api import api_router

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    from .models import User
    from .core.security import hash_pw
    from sqlalchemy import select
    async with AsyncSessionLocal() as s:
        r = await s.execute(select(User).where(User.email == settings.ADMIN_EMAIL))
        if not r.scalar_one_or_none():
            s.add(User(email=settings.ADMIN_EMAIL, name="Dealix Admin", hashed_password=hash_pw(settings.ADMIN_PASSWORD), role="SUPER_ADMIN"))
            await s.commit()
            print("Admin user created: " + settings.ADMIN_EMAIL)

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION, docs_url="/docs")
app.add_middleware(CORSMiddleware, allow_origins=settings.CORS_ORIGINS, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(api_router, prefix="/api")

@app.on_event("startup")
async def startup():
    await init_db()
    print(f"\n{'='*50}")
    print(f"  DEALIX API v{settings.APP_VERSION}")
    print(f"  Admin: {settings.ADMIN_EMAIL}")
    print(f"{'='*50}\n")

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "dealix-api", "version": "1.0.0"}

@app.get("/")
async def root():
    return {"name": "Dealix API", "version": settings.APP_VERSION, "docs": "/docs", "health": "/health"}
