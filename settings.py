from pydantic import BaseSettings

class Settings(BaseSettings):
    # FastAPI application settings
    APP_HOST: str = "0.0.0.0"  # Host IP
    APP_PORT: int = 8000  # Port to run the FastAPI application
    DEBUG: bool = False  # Debug mode (set to True during development)

    # Database settings (if used)
    DATABASE_URL: str = "sqlite:///./my_database.db"  # Database connection URL

    # API settings
    API_PREFIX: str = "/api"  # API URL prefix

    class Config:
        env_file = ".env"  # Load additional settings from a .env file if present

# Create an instance of the Settings class to access the settings
settings = Settings()
