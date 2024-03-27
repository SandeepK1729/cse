from pathlib import Path
import dj_database_url
from datetime import timedelta
import environ
env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ['*']
CORS_ORIGIN_WHITELIST = [
    "http://localhost:3000",
    env.str('FRONTEND_URL', default = 'http://localhost:3000'),
]

# change the setting of append slash 

APPEND_SLASH = False
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'core',
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    
    "crispy_forms",
    "crispy_bootstrap5",

    
    'htmx',          # for htmx
]


CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'corsheaders.middleware.CorsMiddleware',        # corsheaders middleware
]
ROOT_URLCONF = 'cse.urls'

REST_FRAMEWORK = {
     'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',        # simple jwt authentication
      ],
}


ACCESS_TOKEN_LIFETIME_DAYS = env('ACCESS_TOKEN_LIFETIME', cast = int, default = 30)
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days = ACCESS_TOKEN_LIFETIME_DAYS),
    'REFRESH_TOKEN_LIFETIME': timedelta(days = ACCESS_TOKEN_LIFETIME_DAYS + 1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    "UPDATE_LAST_LOGIN": False,

    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": SECRET_KEY,
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    "TOKEN_OBTAIN_SERIALIZER": "core.serializers.MyTokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / "cse" / "templates",
        ],
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

WSGI_APPLICATION = 'cse.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

def get_DB(DB_env):

    # production
    if DB_env == 'online' or DB_env == 'production':
        return dj_database_url.parse(env('DATABASE_URL'))
    
    # development, qa and testing
    elif DB_env in ['dev', 'development', 'qa', 'quality_assurance', 'test', 'testing']:
        return dj_database_url.parse(env('DATABASE_URL_QA'))

    # local
    return {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'cse' / 'db.sqlite3',
            }

DATABASES = {
    'default': get_DB(env('DATABASE_TYPE', default = 'online'))
}
# enable connection pooling
DATABASES['default']['CONN_MAX_AGE'] = 600



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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
MEDIA_URL = 'media/'

STATIC_ROOT = BASE_DIR / 'cse' / 'static_cdn'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# MEDIA_ROOT = STATIC_URL / 'media'

ADMIN_MEDIA_URL = STATIC_URL + 'admin/' # admin is now served by staticfiles


STATICFILES_DIRS = [
    BASE_DIR / 'cse' / STATIC_URL,
]

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"  # new

AUTH_USER_MODEL = 'core.User'

LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

CSE_API_KEY = env('CSE_API_KEY')
CSE_CX = env('CSE_CX')
CSE_URL = env('CSE_URL')

CSE_PARAMS = {
    'key' : CSE_API_KEY,
    'cx' : CSE_CX,
}


MODEL = None
TOKENIZER = None
MODEL_VERSION = env('MODEL_VERSION', cast = str, default = 'v1')
TOKENIZING_APPROACH = 'yake'
THRESHOLD_BACKTRACK_HISTORY = 5
PARAMS = 1000



