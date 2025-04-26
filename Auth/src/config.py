from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "My App"

    DB_URL: str = "sqlite+aiosqlite:///database.db"

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    SECRET_KEY: str = 'R$#%$^%U&I^%^U$%Y#T$@#R#%H$^J%&^*&O(*P)*(O&*I^&%^$%#$@#'
    ALGORITHM: str = 'HS256'

    ACCESS_EXPIRE: int = 60 * 24 * 7
    REFRESH_EXPIRE: int = 60 * 24 * 30


settings = Settings()
