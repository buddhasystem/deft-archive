# Django settings for deft project.
import dbaccess # not in SVN, contact developers (M.Potekhin)
import os, sys, commands


django_path=os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]

## django_path=base_path+os.sep+'panda-deft/deft-ui/web'
## if not os.path.exists(django_path):
##     django_path=base_path+os.sep+'panda-deft/deft-ui/trunk/web'
## if not os.path.exists(django_path):
##     django_path=base_path+os.sep+'Code/panda/panda-deft/deft-ui/trunk/web'


sys.path.append(django_path+os.sep+'utils')

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DEFAULT_CONTENT_TYPE = 'text/html'

ADMINS = (
    ('Maxim Potekhin', 'potekhin@bnl.gov'),
    ('Alden Stradling', 'Alden.Stradling@cern.ch'),
)

MANAGERS = ADMINS

# simple custom code to cover the needs of DB access and application configuration,
# really the best place to put it:
#
# 1.
DATABASES = dbaccess.dbaccess()
# 2.
APP_SETTINGS = {
'deft.home'		: {'default_template':'deft_home_mini'},
'meta.meta'		: {'default_template':'deft_meta'},
'meta.task'		: {'default_template':'deft_task'},
'meta.lib'		: {'default_template':'deft_lib'},
'meta.editmeta'		: {'default_template':'deft_editmeta'},
'meta.metadetail'	: {'default_template':'deft_metadetail'},
'meta.taskdetail'	: {'default_template':'deft_taskdetail'},
'meta.help'		: {'default_template':'deft_help'},
'mcprod.files'  : { 'status_json': 'http://atlas-project-mc-production.web.cern.ch/atlas-project-mc-production/requests/status.json' , #  django_path+os.sep+'mcprod'+os.sep+'status.json',
                    'panda_links': django_path+os.sep+'mcprod'+os.sep+'panda_links.csv'},
'mcprod.auth'   : { 'user': 'bigpandamontestuser',
                    'password': 'Y8NLCmjHROqMIRWk'}
}
# 3.
RUNNING_DEVSERVER = False
STATIC_LOCATION = '/static'
try:
    RUNNING_DEVSERVER = (sys.argv[1] == 'runserver')
    STATIC_LOCATION = 'static'
except:
    pass


# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.4/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Zurich'

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
    django_path+os.sep+'static',
    django_path+os.sep+'jedi'+os.sep+'static',
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'xde6g2f%^7z%z#z+edp)h!c*bw98fi)4(k@e-+f2g!tpmmj=7n'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'deft.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'deft.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    django_path+"/meta/templates",
    django_path+"/deft/templates",
    django_path+"/jedi/templates",
    django_path+"/core/templates",
    django_path+"/prodtask/templates",
    django_path+"/mcprod/templates",
    django_path+"/groupInterface/templates",
    django_path+"/groupInterface/templates/groupInterface",
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'meta',
    'jedi',
    'mcprod',
    'prodtask',
    'core',
    'groupInterface',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
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
