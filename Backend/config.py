# config.py


class Config:
    JWT_SECRET_KEY = "jwt_secret_key"
    SECRET_KEY = "super-secret"
    SQLALCHEMY_DATABASE_URI = "sqlite:///demo.db"
    JWT_ACCESS_TOKEN_EXPIRES = 3600

    CACHE_TYPE= 'RedisCache'
    CACHE_REDIS_URL= 'redis://localhost:6379/3'
    CACHE_DEFAULT_TIMEOUT= 300