from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = 'FastKart E-Commerce API'
    app_version: str = "1.0.0"
    debug:bool = True
    app_description: str = 'E-commerce backend built with FastAPI and Postgresql'
    database_url: str

    jwt_secret_key: str
    jwt_algorithm: str = 'HS256'
    access_token_expire_minutes: int = 30
    redis_url: str = "redis://localhost:6379/0"

    model_config = SettingsConfigDict(
        env_file = '.env',
        extra='ignore'
    )

settings = Settings()