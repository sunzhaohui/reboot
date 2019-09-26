"""
Django settings for reboot project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2$7%v9#_r1yo1f&&0mwqf9sr2mct2-6#$+krd-4urdiw*=4d9*'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = True

ALLOWED_HOSTS = ['*']

# 跳转中间页
JUMP_PAGE = "jump.html"


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'users.apps.UsersConfig',
    'users',
    'pure_pagination',
    'work_order',
    'deploy',
     'djcelery',     # celery自带的app，非常强大
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'reboot.urls'
AUTH_USER_MODEL = 'users.UserProfile'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates'),],
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

WSGI_APPLICATION = 'reboot.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    #'default': {
    #    'ENGINE': 'django.db.backends.sqlite3',
    #    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    #}
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'reboot',
        'USER': 'root',
        'PASSWORD': 'root123',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }

}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

if DEBUG:
    STATICFILES_DIRS = (os.path.join(BASE_DIR,'static'),)

# 在哪找——静态文件存放位置,STATIC_ROOT必须是绝对路径
if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, "static/")
else:
    STATIC_ROOT = ''



# 用访问的URL
MEDIA_URL = '/media/'
# 文件存储的位置例如model中定义的文件存储位置为 reboot/media/orderfiles/2019/06/aa.txt
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# 2.5MB - 2621440
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# 50MB - 5242880
# 100MB 104857600
# 250MB - 214958080
# 500MB - 429916160
MAX_UPLOAD_SIZE = 5242880


# GITLAB
GITLAB_HTTP_URI = "http://123.56.73.115"
GITLAB_TOKEN = "4iBGCWuTtG2Q6VQ5yBYD"

#mygitlab
EXMAPLE_HTTP_URI = 'http://gitlab.example.com'
EXMAPLE_TOKEN = 'x7s5SR8SasHg6szFRWrn'

#jenkinsapi
Jenkins_Url = 'http://172.33.0.82:8080'
Jenkins_User = 'admin'
Jenkins_Password = 'admin'
Jenkins_Token = '1142b7d1b6b9b486fb8147a423f124fa85'

#pyton-jenkins
JENKINS_URL= 'http://172.33.0.82:8080'
JENINS_TOKEN = '1142b7d1b6b9b486fb8147a423f124fa85'
JENKINS_USERNAME = 'admin'
JENKINS_PASSWORD = 'admin'


# 日志
LOGGING = {
    "version": 1,
    'disable_existing_loggers': False,

    "loggers":{
        "reboot": {
            "level": "DEBUG",
            "handlers": ["reboot_file_handle"],
            'propagate': True,
        },

        "django":{
            "level": "DEBUG",
            "handlers": [ "django_handle"],
            'propagate': True,
        },

        "report":{
            "level": "ERROR",
            "handlers": [ "mail"],
            'propagate': True,
        }
    },

    "handlers": {

        "reboot_file_handle": {
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs", "reboot.log"),
            "formatter": "reboot"
        },

        "django_handle": {
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs", "django.log"),
            "formatter": "reboot"
        },

        'django_request_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, "logs", 'request.log'),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'reboot',
        },

        "mail": {
            "class": "logging.handlers.SMTPHandler",
            "level": "ERROR",
            "formatter": "simple",
            "mailhost": ("smtp.139.com", 25),
            "fromaddr": "13260071987@139.com",
            "toaddrs": ["787696331@qq.com"],
            "subject": "devops mail",
            "credentials": ("13260071987@139.com", "yi15093547036")
        }
    },

    'formatters': {
        'reboot':{
            'format': '[%(asctime)s] [%(process)d] [%(thread)d] [%(filename)16s:%(lineno)4d] [%(levelname)-6s] %(message)s'
        },
        'simple': {
            'format': '%(asctime)s %(levelname)s %(message)s'
        }
    },

}


# 邮件
EMAIL_HOST = "smtp.exmail.qq.com"
EMAIL_PORT = 465
EMAIL_HOST_USER = "sa-notice@yuanxin-inc.com"
EMAIL_HOST_PASSWORD = "Miao13456"
EMAIL_USE_SSL = True
EMAIL_FROM = "sa-notice@yuanxin-inc.com"



import djcelery
djcelery.setup_loader()         # 加载djcelery

BROKER_URL = 'redis://172.20.80.93:6379/2'     # redis作为中间件
BROKER_TRANSPORT = 'redis'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'     # Backend数据库

#CELERYD_LOG_FILE = BASE_DIR + "/logs/celery/celery.log"         # log路径
CELERYD_LOG_FILE = os.path.join(BASE_DIR,"logs/celery/celery.log")
print(CELERYD_LOG_FILE)
#CELERYBEAT_LOG_FILE = BASE_DIR + "/logs/celery/beat.log"     # beat log路径
CELERYBEAT_LOG_FILE = os.path.join(BASE_DIR,"logs/celery/beat.log")
print(CELERYBEAT_LOG_FILE)





PAGINATION_SETTINGS = {'SHOW_FIRST_PAGE_WHEN_INVALID': True}
# 无效页面时，显示第一页而不是404页面

AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.AllowAllUsersModelBackend']
