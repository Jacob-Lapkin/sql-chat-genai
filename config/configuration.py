from dotenv import load_dotenv
import os

SECRET_KEY = os.getenv("SECRET_KEY")
class Config:
    DEBUG = True
    VERSION = 'v1.1'
    HOSTNAME = "insights"
    SECRET_KEY = SECRET_KEY

class Development(Config):
    DEBUG = True

class Production(Config):
    DEBUG = False