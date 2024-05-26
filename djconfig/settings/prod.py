from .base import *

STATICS_APPS.insert(0, "whitenoise.runserver_nostatic")

MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.environ.get("POSTGRES_HOST", '127.0.0.1'),
        "NAME": os.environ.get('POSTGRES_NAME', 'dtb_db'),
        "USER": os.environ.get("POSTGRES_USER", 'dtb_user'),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", 'dtb_user'),
        "PORT": os.environ.get("POSTGRES_PORT", '5432')
    }
}
