from .base import *

STATICS_APPS.insert(0, "whitenoise.runserver_nostatic")

MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.environ.get("POSTGRES_HOST", 'localhost'),
        "NAME": os.environ.get('POSTGRES_NAME', 'postgres'),
        "USER": os.environ.get("POSTGRES_USER", 'postgres'),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", 'postgres'),
        "PORT": os.environ.get("POSTGRES_PORT", '5432')
    }
}
