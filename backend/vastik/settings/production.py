"""
VASTIK — Production Settings
"""
from .base import *  # noqa: F401, F403

DEBUG = False

# PostgreSQL required in production
DATABASES = {
    'default': env.db('DATABASE_URL')
}

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=True)

# Whitenoise for static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
