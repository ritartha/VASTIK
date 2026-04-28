"""
VASTIK — Base Django Settings
Shared across all environments.
"""
import os
from pathlib import Path
import environ

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # backend/
PROJECT_DIR = BASE_DIR.parent  # VASTIK/

# Initialize environ
env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, ['localhost', '127.0.0.1']),
)

# Read .env file — check project root first, then backend dir
# On Railway, env vars are set in the dashboard so .env may not exist
ENV_FILE = PROJECT_DIR / '.env'
if ENV_FILE.exists():
    environ.Env.read_env(str(ENV_FILE))
elif (BASE_DIR / '.env').exists():
    environ.Env.read_env(str(BASE_DIR / '.env'))

# Security
SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
ALLOWED_HOSTS = env('ALLOWED_HOSTS')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party
    'rest_framework',
    'corsheaders',
    # Local apps
    'store',
    'gallery',
    'contact',
    'testimonials',
    'sl_bridge',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'vastik.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'vastik.context_processors.social_links',
            ],
        },
    },
]

WSGI_APPLICATION = 'vastik.wsgi.application'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    PROJECT_DIR / 'frontend' / 'static',
]
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ── Django REST Framework ─────────────────────────────────────────────────────
# Authentication classes are intentionally empty:
#   - All API endpoints use their own OTP / signed-token / shared-secret auth
#   - SessionAuthentication (DRF default) enforces Django CSRF on every POST
#     that carries a session cookie, causing 403 Forbidden in production where
#     CSRF_COOKIE_SECURE=True and DEBUG=False.
#   - The Django admin is unaffected — it has its own CSRF handling via
#     CsrfViewMiddleware in MIDDLEWARE above.
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# CORS
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[
    'http://localhost:8000',
    'http://127.0.0.1:8000',
])
CORS_ALLOW_ALL_ORIGINS = DEBUG

# Social media links (injected into templates via context processor)
SOCIAL_LINKS = {
    'facebook': env('SOCIAL_FACEBOOK', default='#'),
    'discord': env('SOCIAL_DISCORD', default='#'),
    'instagram': env('SOCIAL_INSTAGRAM', default='#'),
    'flickr': env('SOCIAL_FLICKR', default='#'),
    'sl_profile': env('SOCIAL_SL_PROFILE', default='#'),
}

# Second Life Bridge
SL_BRIDGE_SECRET = env('SL_BRIDGE_SECRET', default='')

# Discord Webhook (for contact message notifications)
DISCORD_WEBHOOK_URL     = env('DISCORD_WEBHOOK_URL',     default='')
DISCORD_THUMBNAIL_IMAGE = env('DISCORD_THUMBNAIL_IMAGE', default='')
DISCORD_FOOTER_IMAGE    = env('DISCORD_FOOTER_IMAGE',    default='')
