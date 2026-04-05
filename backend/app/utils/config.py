from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "VocaCare"
    MONGODB_URL: str = "mongodb://Stuttering_mongo_db:ijDuRLkzRwDcEBfQ@ac-p2asiz6-shard-00-00.e1yilpv.mongodb.net:27017,ac-p2asiz6-shard-00-01.e1yilpv.mongodb.net:27017,ac-p2asiz6-shard-00-02.e1yilpv.mongodb.net:27017/?ssl=true&replicaSet=atlas-ym72hj-shard-0&authSource=admin&appName=Stuttering"
    DATABASE_NAME: str = "Stuttering"
    SECRET_KEY: str = "YOUR_SUPER_SECRET_KEY_KEEP_IT_SAFE"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
