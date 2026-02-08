from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database configuration
    database_url: str = Field(
        default="postgresql+asyncpg://username:password@localhost/dbname",
        description="Database connection string"
    )

    # Neon PostgreSQL configuration (recommended for this project)
    neon_database_url: Optional[str] = Field(
        default=None,
        description="Neon PostgreSQL connection string"
    )

    # OpenAI configuration
    openai_api_key: str = Field(
        default="your_openai_api_key_here",
        description="OpenAI API key"
    )
    openai_model: str = Field(
        default="gpt-4o",
        description="OpenAI model to use"
    )

    # Authentication configuration
    secret_key: str = Field(
        default="your_secret_key_here_generate_a_strong_one",
        description="Secret key for JWT tokens"
    )
    algorithm: str = Field(
        default="HS256",
        description="Algorithm for JWT encoding"
    )
    access_token_expire_minutes: int = Field(
        default=30,
        description="Access token expiration in minutes"
    )

    # Better Auth configuration
    better_auth_secret: str = Field(
        default="your_better_auth_secret",
        description="Better Auth secret"
    )
    better_auth_url: str = Field(
        default="http://localhost:8000",
        description="Better Auth URL"
    )

    # Application configuration
    app_name: str = Field(
        default="Todo AI Chatbot",
        description="Name of the application"
    )
    api_v1_str: str = Field(
        default="/api/v1",
        description="API version prefix"
    )
    debug: bool = Field(
        default=False,
        description="Debug mode"
    )

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create a single instance of settings
settings = Settings()