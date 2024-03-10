import sys
from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))  # 把项目根目录插入到sys.path的最前面
sys.path.insert(0, str(BASE_DIR / "apps"))  # 把apps目录也插入到sys.path中，可以直接导入应用

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-l5k!rt+k!=ha)sdx-&chy)f6l!ys-5#!unpph7)#i9emlc4r7b"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]  # 允许所有主机访问
# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",  # DRF
    "rest_framework_simplejwt",  # JWT认证
    "rest_framework_simplejwt.token_blacklist",  # JWT黑名单
    "django_comment_migrate",  # 注释迁移
    "drf_yasg",  # drf文档
    "apps.system.users.apps.UsersConfig",
    "apps.system.menus.apps.MenusConfig",
    "apps.system.roles.apps.RolesConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "mortal.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "mortal.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "mortal",
        "HOST": "127.0.0.1",
        "PORT": 3306,
        "USER": "root",
        "PASSWORD": "root",
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "zh-hans"

TIME_ZONE = "Asia/Shanghai"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# DRF配置
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    # drf_yasg配置
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}

# JWT配置
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=7),  # token有效期
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),  # 刷新token有效期
    "ROTATE_REFRESH_TOKENS": True,  # 是否刷新token
    "BLACKLIST_AFTER_ROTATION": True,  # 刷新token后，旧token失效
}

# CORS配置
CORS_ALLOW_ORIGINS = ["*"]  # 允许跨域的域名列表，*代表允许所有域名跨域访问

# 日志配置
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    # 日志格式集合
    "formatters": {
        # 详细的日志格式
        "verbose": {"format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"},
        # 简单的日志格式
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    # 过滤器
    "filters": {
        "require_debug_true": {
            # 只有在Debug为True时才启用
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    # 处理器
    "handlers": {
        # 在终端打印
        "console": {
            "level": "DEBUG",
            "filters": ["require_debug_true"],  # 只有在Debug为True时才启用
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        # 默认的
        "default": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": BASE_DIR / "logs/default.log",  # 日志输出文件
            "maxBytes": 1024 * 1024 * 5,  # 文件大小
            "backupCount": 5,  # 备份份数
            "formatter": "verbose",
            "encoding": "utf-8",
        },
        # error日志
        "error": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": BASE_DIR / "logs/error.log",  # 日志输出文件
            "maxBytes": 1024 * 1024 * 5,  # 文件大小
            "backupCount": 5,  # 备份份数
            "formatter": "verbose",
            "encoding": "utf-8",
        },
    },
    # 日志记录器
    "loggers": {
        # django内置的logger应用如下配置
        "django": {
            "handlers": ["default", "error", "console"],
            "level": "INFO",
            "propagate": True,
        },
    },
}
# 指定项目中的用户模型
AUTH_USER_MODEL = "users.User"
