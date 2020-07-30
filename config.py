import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Caching
    # Desativa o cache por padrão quando não estiver em produção
    CACHE_TYPE = os.environ.get("CACHE_TYPE", "null")

    CURRENT_MONTH = os.environ["CURRENT_MONTH"]
    CURRENT_YEAR = os.environ["CURRENT_YEAR"]


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_POOL_RECYCLE = int(os.environ.get("SQLALCHEMY_POOL_RECYCLE", 299))
    SQLALCHEMY_POOL_TIMEOUT = int(os.environ.get("SQLALCHEMY_POOL_TIMEOUT", 20))
    # Cache config
    CACHE_TYPE = os.environ.get("CACHE_TYPE", "filesystem")
    CACHE_DIR = os.environ.get("CACHE_DIR", ".flaskcache/")
    CACHE_DEFAULT_TIMEOUT = 0


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
