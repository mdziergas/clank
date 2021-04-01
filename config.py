
import os
class Config(object):
    DEBUG=os.environ.get("DEBUG")
    TESTING=os.environ.get("DEBUG")
    MONGO=os.environ.get("MONGO")
    
    
class ProductionConfig(Config):
    DEBUG=os.environ.get("DEBUG")
    SECRET_KEY=os.environ.get("SECRET_KEY")
   
class DevelopmentConfig(Config):
    DEBUG=os.environ.get("DEBUG")
    ENV=os.environ.get("FLASK_ENV")
    DEVELOPMENT=True
    SECRET_KEY=os.environ.get("SECRET_KEY")
  
CONFIGS = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}