"""
VASTIK — Development Settings
"""
from .base import *  # noqa: F401, F403

DEBUG = True

# Use SQLite for development if DATABASE_URL is not set
DATABASES = {
    'default': env.db('DATABASE_URL', default=f'sqlite:///{BASE_DIR / "db.sqlite3"}')
}

# Simpler static file storage for development
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Email — print to console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Disable CORS restrictions in dev
CORS_ALLOW_ALL_ORIGINS = True
