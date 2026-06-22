from .base import *
import environ


env = environ.Env()

environ.Env.read_env(BASE_DIR / ".env")

ALLOWED_HOSTS = []

SECRET_KEY = env("SECRET_KEY")

DEBUG = env.bool("DEBUG")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}