import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("FLASK_APP_SECRET_KEY")


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.environ.get('POSTGRES_USER')}:{os.environ.get('POSTGRES_PASSWORD')}@{os.environ.get('POSTGRES_HOST')}:{os.environ.get('POSTGRES_PORT')}/{os.environ.get('POSTGRES_DB')}"


class ProductionConfig(Config):
    if os.environ.get("DATABASE_URL") is not None:
        SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL").replace(
            "://", "ql://", 1
        )


config = {"development": DevelopmentConfig, "production": ProductionConfig}
