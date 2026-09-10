from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = 'FastKart E-Commerce API'
    app_version: str = "1.0.0"
    debug:bool = True
    app_description: str = 'E-commerce backend built with FastAPI and Postgresql'

    model_config = SettingsConfigDict(
        env_files = '.env',
        extra='ignore'
    )

settings = Settings()