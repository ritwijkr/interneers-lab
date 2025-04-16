import mongoengine
from mongoengine import connect

SECRET_KEY = "test-secret-key"
DEBUG = True
INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "product",  # for example
]
USE_TZ = True
TIME_ZONE = "UTC"

MONGODB_NAME = "test_db"
MONGODB_HOST = "mongodb://localhost:27017/"  
connect(db=MONGODB_NAME, host=MONGODB_HOST)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.dummy"
    }
}
