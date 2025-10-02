import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "supersecretkey")
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://taskuser:NewPassword123!@localhost/taskdb"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "jwtsecretkey")
    CACHE_TYPE = "SimpleCache"  # You can use RedisCache if Redis is set up
    CACHE_DEFAULT_TIMEOUT = 300
