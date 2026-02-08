import os
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import settings
from config.settings import settings
from config.constants import *

# Import API routers
from api.chat import router as chat_router
from api.auth import router as auth_router
from api.threads import router as threads_router
from api.tasks import router as tasks_router

# Import database
from database.connection import engine
from models.user import User  # noqa: F401
from models.task import Task  # noqa: F401
from models.thread import Thread  # noqa: F401
from models.message import Message  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown events."""
    # Startup: Initialize database tables
    print("Initializing database...")
    from sqlmodel import SQLModel
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield

    # Shutdown: Cleanup
    await engine.dispose()


def create_app():
    """Create and configure FastAPI application."""
    app = FastAPI(
        title=settings.app_name,
        description="AI-powered todo chatbot with natural language processing",
        version="0.1.0",
        lifespan=lifespan,
        debug=settings.debug
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, configure this properly
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routers
    app.include_router(chat_router, prefix=settings.api_v1_str)
    app.include_router(auth_router, prefix=settings.api_v1_str)
    app.include_router(threads_router, prefix=settings.api_v1_str)
    app.include_router(tasks_router, prefix=settings.api_v1_str)

    @app.get("/")
    async def root():
        return {"message": f"Welcome to {settings.app_name}"}

    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "service": settings.app_name}

    return app


# Create the application instance
app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True,
        log_level="info"
    )