from pydantic_settings import BaseSettings


class Config(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    SECRET_KEY: str
    ALGORYTHM: str

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    DB_TEST_HOST: str
    DB_TEST_PORT: int
    DB_TEST_USER: str
    DB_TEST_PASS: str
    DB_TEST_NAME: str

    @property
    def TEST_DATABASE_URL(self):
        return (f"postgresql+asyncpg://{self.DB_TEST_USER}:{self.DB_TEST_PASS}@{self.DB_TEST_HOST}:"
                f"{self.DB_TEST_PORT}/{self.DB_TEST_NAME}")

    class Config:
        env_file = '.env'


config = Config()
