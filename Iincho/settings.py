"""
Django settings for Iincho project.

Generated by 'django-admin startproject' using Django 1.8.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import dj_database_url
from social.pipeline import DEFAULT_AUTH_PIPELINE

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('IINCHO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG') == '1'
ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social.apps.django_app.default',
    'core',
    'accounts',
    'web',
    'categories',
    'articles',
    'django_jinja',
    'attachments',
    'bootstrapform_jinja',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'Iincho.urls'

TEMPLATES = [
    {
        "BACKEND": "django_jinja.backend.Jinja2",
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "match_extension": None,
            "match_regex": r"^(?!admin/).*\.jinja.{0,1}$",
            "app_dirname": "templates",
            # Can be set to "jinja2.Undefined" or any other subclass.
            "undefined": None,
            "autoescape": True,
            "auto_reload": DEBUG,
            'context_processors': [
                'django.core.context_processors.csrf',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.core.context_processors.media',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # social-auth
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
            ],
            "filters": {
                "max": "core.filters.maximum",
                "min": "core.filters.minimum",
                "datetimeformat": "core.filters.datetimeformat",
                "category_tree": "categories.filters.category_tree",
                "split_category_nodes": "categories.filters.split_nodes",
                "remove_param_str": "core.filters.remove_param_str",
            },

        }
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # social-auth
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'Iincho.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = {'default': dj_database_url.config(
    default='sqlite:///%s' % os.path.join(BASE_DIR, 'db.sqlite3'))}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True
USE_L10N = True
USE_TZ = False

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'sitestatic')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

AUTHENTICATION_BACKENDS = (
    'social.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_REDIRECT_URL = '/'

# AUTH_USER_MODEL = 'accounts.CustomUser'

# social-auth
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get('GOOGLE_OAUTH2_CLIENT_ID')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get('GOOGLE_OAUTH2_CLIENT_SECRET')

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'accounts.pipelines.get_user_avatar',
)

SOCIAL_AUTH_WHITELISTED_DOMAINS = os.environ.get('AUTH_WHITELISTED_DOMAINS', '').split()
SOCIAL_AUTH_WHITELISTED_EMAILS = os.environ.get('AUTH_WHITELISTED_EMAILS', '').split()

# media
MEDIA_ROOT = os.path.join(BASE_DIR, 'site_media/')
MEDIA_URL = '/media/'

# logging
LOGGING = {
    'version': 1,
    'formatters': {  # 出力フォーマット
        'all': {
            'format': '\t'.join([
                "[%(levelname)s]",
                "asctime:%(asctime)s",
                "module:%(module)s",
                "message:%(message)s",
                "process:%(process)d",
                "thread:%(thread)d",
            ])
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            # 標準出力
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'command': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },

    },
}

FIXTURE_DIRS = (
    os.path.join(BASE_DIR, 'fixtures'),
)
