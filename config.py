from pydantic import BaseSettings


class Settings(BaseSettings):
    postgres_port: int
    database_url: str
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str


    class Config:
        env_file = '.env'

settings = Settings()
