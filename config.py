from pydantic import BaseSettings


class Settings(BaseSettings):
    postgres_port: int
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_server: str


    class Config:
        env_file = 'local.env'

settings = Settings()
