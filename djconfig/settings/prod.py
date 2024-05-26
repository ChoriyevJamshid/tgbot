from .base import *

STATICS_APPS.insert(0, "whitenoise.runserver_nostatic")

MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"






