from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.accounts import router as accounts_router
from app.api.routes.campaigns import router as campaigns_router
from app.api.routes.health import router as health_router
from app.api.routes.oauth import router as oauth_router
from app.api.routes.posts import router as posts_router
from app.api.routes.queue import router as queue_router
from app.api.routes.videos import router as videos_router
from app.core.config import settings


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Social Media Automation API",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.frontend_url,
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# API ROUTES
# ============================================================

app.include_router(
    health_router,
    prefix="/api",
)

app.include_router(
    accounts_router,
    prefix="/api",
)

app.include_router(
    videos_router,
    prefix="/api",
)

app.include_router(
    campaigns_router,
    prefix="/api",
)

app.include_router(
    posts_router,
    prefix="/api",
)

app.include_router(
    queue_router,
    prefix="/api",
)

app.include_router(
    oauth_router,
    prefix="/api",
)


# ============================================================
# ROOT
# ============================================================

@app.get("/")
async def root():
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running",
    }
