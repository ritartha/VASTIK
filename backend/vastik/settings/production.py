"""
VASTIK — Production Settings (Railway Deployment)
"""
from .base import *  # noqa: F401, F403

DEBUG = False

# ── Hosts & Security ──────────────────────────────────────────
# Railway provides RAILWAY_PUBLIC_DOMAIN automatically
RAILWAY_DOMAIN = env('RAILWAY_PUBLIC_DOMAIN', default='')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])
if RAILWAY_DOMAIN:
    ALLOWED_HOSTS.append(RAILWAY_DOMAIN)
# Always allow health checks from Railway
ALLOWED_HOSTS.append('.railway.app')

# CSRF trusted origins (required for Django 4.0+ with HTTPS)
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=[])
if RAILWAY_DOMAIN:
    CSRF_TRUSTED_ORIGINS.append(f'https://{RAILWAY_DOMAIN}')

# CORS — allow your frontend domain
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[])
if RAILWAY_DOMAIN:
    CORS_ALLOWED_ORIGINS.append(f'https://{RAILWAY_DOMAIN}')

# ── Database — PostgreSQL via DATABASE_URL ────────────────────
DATABASES = {
    'default': env.db('DATABASE_URL')
}

# ── Security Headers ─────────────────────────────────────────
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Railway handles SSL termination at the proxy level,
# so we do NOT redirect at the Django level — it causes redirect loops
SECURE_SSL_REDIRECT = False
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# ── Static Files (Whitenoise) ────────────────────────────────
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# ── Logging ──────────────────────────────────────────────────
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'sl_bridge': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
