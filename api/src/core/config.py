import os
from logging import config as logging_config
from pydantic import BaseSettings, Field

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    # Redis
    REDIS_HOST: str = Field('127.0.0.1', env='REDIS_HOST')
    REDIS_PORT: int = Field(6379, env='REDIS_PORT')
    # Elastic
    ELASTIC_HOST: str = Field('127.0.0.1', env='EL_HOST')
    ELASTIC_PORT: int = Field(9200, env='EL_PORT')
    # Project
    PROJECT_NAME: str = Field('movies', env='PROJECT_NAME')

    class Config:
        env_file = '.env'


settings = Settings()

# Название проекта. Используется в Swagger-документации
PROJECT_NAME = settings.PROJECT_NAME

# Настройки Redis
REDIS_HOST = settings.REDIS_HOST
REDIS_PORT = settings.REDIS_PORT

# Настройки Elasticsearch
ELASTIC_HOST = settings.ELASTIC_HOST
ELASTIC_PORT = settings.ELASTIC_PORT

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CACHE_EXPIRE_IN_SECONDS = 60 * 5
MESSEGE_NON_FOUND = 'Data not found'
