import os

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///chat.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY") or "My_Strong_Secret_Key"

