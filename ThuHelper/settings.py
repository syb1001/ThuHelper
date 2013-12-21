# coding=utf-8

# Django settings for ThuHelper project.
import os.path
#from bae.core import const
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASE_NAME = "JeeyjPsbXniwEMCMuloW"

if 'SERVER_SOFTWARE' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': DATABASE_NAME,                      # Or path to database file if using sqlite3.
            'USER': 'UXyhLqw1gY77469MXFyEhnGv',                      # Not used with sqlite3.
            'PASSWORD': 'hUL1AZA8dAMCApKpqjqL5YstR3Sgfwsg',                  # Not used with sqlite3.
            'HOST': 'sqld.duapp.com',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '4050',                      # Set to empty string for default. Not used with sqlite3.
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'thuhelper',                      # Or path to database file if using sqlite3.
            'USER': 'root',                      # Not used with sqlite3.
            'PASSWORD': 'hehe921013',                  # Not used with sqlite3.
            'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '3306',                      # Set to empty string for default. Not used with sqlite3.
        }
    }
# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.4/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(__file__), '../static').replace('\\','/'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '2x*dpmtcqb34i(g-k&amp;h0@*%l)@sv4$$wps+yp_+^@kv80id+s+'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    #'django.middleware.common.CommonMiddleware',
    #'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    #'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'ThuHelper.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'ThuHelper.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(__file__), 'templates').replace('\\','/'),
)

INSTALLED_APPS = (
    #'django.contrib.auth',
    #'django.contrib.contenttypes',
    #'django.contrib.sessions',
    #'django.contrib.sites',
    #'django.contrib.messages',
    #'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'ThuHelper',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# 项目配置
# 开发者凭据
APPID = 'wx908467c39426e3bc'
APP_SECRET = '82729dab279ea74bab044cd868ec1543'
# 与微信公众平台约定的token
# 在微信平台上填写
WEIXIN_TOKEN = 'helloworld'
# 人文社科图书馆座位查询URL
URL_LIBRARY = 'http://thuhelper11.duapp.com/library/'
URL_LIBRARY_IMAGE_PREF = 'http://thuhelper11.duapp.com/static/images/library/library'
MAX_LIBRARY_IMAGE_INDEX = 4

# 美食图片URL
URL_FOOD_IMAGE_PREF = 'http://thuhelper11.duapp.com/static/images/food/'

# 音乐图文消息大图
URL_PLAYER_PREF = 'http://thuhelper11.duapp.com/musicplay'
URL_MUSIC_IMAGE_PREF = 'http://thuhelper11.duapp.com/static/images/music/music_'
URL_MUSIC_IMAGE_SUF = '.jpg'
MAX_MUSIC_IMAGE_INDEX = 5
# 音乐图文消息分类小图
URL_MUSIC_NOTE_IMAGE_PREF = 'http://thuhelper11.duapp.com/static/images/music_notes/'
MAX_MUSIC_NOTE_IMAGE_INDEX = {'1': 3, '2': 3, '3': 3}
# 音乐图文消息随便听听图片
URL_MUSIC_GIFT_IMAGE_PREF = 'http://thuhelper11.duapp.com/static/images/gift/gift'
MAX_MUSIC_GIFT_IMAGE_INDEX = 3

# 默认专辑图片
URL_ALBUM_PREF = 'http://thuhelper11.duapp.com/static/images/album/album'
MAX_ALBUM_IMAGE_INDEX = 5

# 帮助信息列表
URL_HELP = 'http://thuhelper11.duapp.com/help/'
URL_HELP_IMAGE = 'http://thuhelper11.duapp.com/static/images/hand.jpg'
URL_HELP_IMAGE_PREF = 'http://thuhelper11.duapp.com/static/images/help/'

# 关于我们页面
URL_ABOUT = 'http://thuhelper11.duapp.com/about/'

EXPRESSION_LIST = {
    'a': ['/::)', '/::B', '/:8-)', '/::P', '/::D', '/::+', '/:,@P', '/:,@-D', '/::>', '/::,@', '/:handclap', '/:B-)', '/::*'],
    'b': ['/::|', '/::Z', '/:–b', '/::d', '/:|-)', '/::-O', '/:@x', '/:8*'],
    'c': ['/::~', '/::<', '/::X', '/::’(', '/::(', '/::T', '/::g', '/::L', '/:,@!', '/:xx', '/:P-(', '/::’|'],
    'd': ['/::-|', '/::@', '/::O', '/::Q', '/:,@o', '/::!', '/:,@f', '/::-S', '/::8', '/:!!!'],
    'e': ['/::$', '/:?', '/:,@x', '/:,@@', '/:wipe', '/:dig', '/:&-(', '/:<@', '/:@>', '/:>-|', '/:X-)'],
    'f': ['/:bye'],
}