import os
from pathlib import Path
from celery.schedules import crontab
from dotenv import load_dotenv
import dj_database_url

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    "SECRET_KEY", 'django-insecure-t-53qx4*$j5zj$6b#%s!cv-g-380s72^xck@q*^yp8e5)ha!yk'
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", False)
ALLOWED_HOSTS = ["*"]

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
]

STATICS_APPS = [
    'django.contrib.staticfiles',
]

THIRD_PART_APPS = []

LOCAL_APPS = [
    'djapp'
]

INSTALLED_APPS = DJANGO_APPS + STATICS_APPS + LOCAL_APPS + THIRD_PART_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'djconfig.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'djconfig.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DB_SQLITE = 'sqlite'
DB_POSTGRESQL = 'postgresql'

# DB_ALL = {
#     DB_SQLITE: {
#         'default': {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': BASE_DIR / 'db.sqlite3',
#         }
#     },
#     DB_POSTGRESQL: {
#         "ENGINE": "django.db.backends.postgresql",
#         "HOST": os.environ.get("POSTGRES_HOST", 'localhost'),
#         "NAME": os.environ.get('POSTGRES_NAME', 'postgres'),
#         "USER": os.environ.get("POSTGRES_USER", 'postgres'),
#         "PASSWORD": os.environ.get("POSTGRES_PASSWORD", 'postgres'),
#         "PORT": os.environ.get("POSTGRES_PORT", '5432')
#     }
# }
# DATABASES = {
#     "default": DB_ALL[os.environ.get("DJANGO_DB", default=DB_SQLITE)]
# }

# DATABASES = {
#     "default": dj_database_url.config(conn_max_age=600) #, default='sqlite:///db.sqlite3')
# }

DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.environ.get("POSTGRES_HOST", 'localhost'),
        "NAME": os.environ.get('POSTGRES_NAME', 'dtb_db'),
        "USER": os.environ.get("POSTGRES_USER", 'dtb_user'),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", 'dtb_user'),
        "PORT": os.environ.get("POSTGRES_PORT", '5432')
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_TZ = True

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL",
                                   default="redis://localhost:6379/")

# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-result_backend
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_TIMEZONE = TIME_ZONE

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "staticfiles"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CELERY_BEAT_SCHEDULE = {
    'add-every-day': {
        'task': 'djapp.tasks.get_parsing_data',
        'schedule': crontab(day_of_week="*/1", hour="0", minute="0")
    }
}
