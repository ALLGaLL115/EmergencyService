from pydantic_settings import SettingsConfigDict, BaseSettings

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    

    SMTP_HOST: str
    SMTP_PORT: str
    SMTP_USER: str
    SMTP_PASSWORD: str

    CELERY_HOST: str


    RABBITMQ_DEFAULT_HOST: str
    RABBITMQ_DEFAULT_PORT: int
    RABBITMQ_DEFAULT_USER: str
    RABBITMQ_DEFAULT_PASS: str



    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DATABASE_URL_psycopg2(self):
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    @property
    def CELERY_BROKER(self):
        return f"pyamqp://guest@{self.CELERY_HOST}//"

    

model_config = SettingsConfigDict(env_file='.env')

settings = Settings()


# Что по поводу конфигов как ими пользоваться, сколько их должно быть, нужен ли 
# отдельный под Postgresql, reids, celery и такого рода вещей. 
# Как у вас на проектах делают?