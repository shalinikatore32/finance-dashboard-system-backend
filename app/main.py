from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.core.config import settings
from app.db.mongodb import connect_to_mongo, close_mongo_connection
from app.routers import auth, users, transactions, dashboard
from app.middleware.error_handler import add_exception_handlers

# Setup Rate Limiter
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="Backend API for Finance Dashboard with RBAC",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # Rate Limiting
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, change to specific origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Events
    @app.on_event("startup")
    async def startup_db_client():
        await connect_to_mongo()

    @app.on_event("shutdown")
    async def shutdown_db_client():
        await close_mongo_connection()

    # Exception Handlers
    add_exception_handlers(app)

    # Routers
    app.include_router(auth.router, prefix="/api")
    app.include_router(users.router, prefix="/api")
    app.include_router(transactions.router, prefix="/api")
    app.include_router(dashboard.router, prefix="/api")

    @app.get("/health", tags=["health"])
    @limiter.limit("5/minute")
    async def health_check(request: Request):
        return {"status": "ok", "project": settings.PROJECT_NAME}

    return app

app = create_app()
