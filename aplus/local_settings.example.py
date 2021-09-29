#DEBUG = False
#SECRET_KEY = '' # will be autogenerated in secret_key.py if not specified here
#BASE_URL = 'http://localhost:8000/' # required!
#SERVER_EMAIL = 'your_email@domain.com'
#ADMINS = (
#    ('Your Name', 'your_email@domain.com'),
#)

#from os import environ
#APLUS_AUTH = {
#    "PRIVATE_KEY": environ.get("PRIVATE_KEY"),
#    "PUBLIC_KEY": environ.get("PUBLIC_KEY"),
#}
#ALIAS_TO_PUBLIC_KEY={
#    "gitmanager": """-----BEGIN PUBLIC KEY-----
#...
#-----END PUBLIC KEY-----
#""",
#    "grader": """-----BEGIN PUBLIC KEY-----
#...
#-----END PUBLIC KEY-----
#""",
#}
#URL_TO_ALIAS={
#    "gitmanager.example.com": "gitmanager",
#    "grader.example.com": "grader",
#}

# The organization this instance is deployed at.
# Can be used to identify users from home university by comparing this to
# organization information received from Haka login.
#LOCAL_ORGANIZATION = 'aalto.fi'

## Branding
#BRAND_NAME = 'Your brand name (default is A+)'
#BRAND_NAME_LONG = 'Aplus'
#BRAND_DESCRIPTION = 'Description of your service (default is Virtual Learning Environment)'
#BRAND_INSTITUTION_NAME = Your institution name, e.g., 'Aalto University', 'Tampere university'
#BRAND_INSTITUTION_NAME_FI = 'Aalto-yliopisto'
#WELCOME_TEXT = 'Welcome to A+ <small>modern learning environment</small>'
#SHIBBOLETH_TITLE_TEXT = 'Aalto University users'
#SHIBBOLETH_BODY_TEXT = 'Log in with your Aalto University user account by clicking on the button below. FiTech, Open University and programme students as well as staff members must log in here.'
#SHIBBOLETH_BUTTON_TEXT = 'Log in with Aalto account'
#HAKA_TITLE_TEXT = 'Haka Federation users'
#HAKA_BODY_TEXT = 'If your organization is a member of Haka federation, log in by clicking the button below.'
#HAKA_BUTTON_TEXT = 'Log in with Haka'
#MOOC_TITLE_TEXT = 'Users external to Aalto'
#MOOC_BODY_TEXT = 'Some of our courses are open for everyone. Log in with your user account from one of the following services.'
#INTERNAL_USER_LABEL = 'Aalto'
#EXTERNAL_USER_LABEL = 'MOOC'
#LOGIN_USER_DATA_INFO = 'Your personal data are stored in {brand_name}. For additional information, please see <a href="{privacy_url}">the privacy notice</a>.'

#WELCOME_TEXT_FI = 'A+ <small>verkkopohjainen oppimisympäristö</small>'
#SHIBBOLETH_TITLE_TEXT_FI = 'Aalto-yliopiston käyttäjät'
#SHIBBOLETH_BODY_TEXT_FI = 'Kirjaudu palveluun Aalto-yliopiston käyttäjätunnuksella alla olevasta painikkeesta. FiTechin, avoimen yliopiston ja koulutusohjelmien opiskelijoiden sekä henkilökunnan täytyy kirjautua tästä.'
#SHIBBOLETH_BUTTON_TEXT_FI = 'Kirjaudu Aalto-tunnuksella'
#HAKA_TITLE_TEXT_FI = 'Haka-käyttäjät'
#HAKA_BODY_TEXT_FI = 'Jos organisaatiosi on Haka-federaation jäsen, kirjaudu palveluun alla olevasta painikkeesta.'
#HAKA_BUTTON_TEXT_FI = 'Kirjaudu Haka-tunnuksella'
#MOOC_TITLE_TEXT_FI = 'Käyttäjät Aallon ulkopuolelta'
#MOOC_BODY_TEXT_FI = 'Osa kursseistamme on avoinna kaikille. Kirjaudu sisään jonkin seuraavan palvelun käyttäjätunnuksellasi.'
#LOGIN_USER_DATA_INFO_FI = 'Henkilötietosi säilytetään {brand_name}-järjestelmässä. Katso lisätietoja <a href="{privacy_url}">tietosuojailmoituksesta</a>.'

# Show red alert on top of all pages
#SITEWIDE_ALERT_TEXT = "Maintenance on Monday"
#SITEWIDE_ALERT_TEXT = {'en': "Maintenance on Monday", 'fi': "Maanantaina on palvelukatko"}
# Show blue info box on course index and course menu
#SITEWIDE_ADVERT = {
#    'not-before': '2020-01-01', # start showing on 1st
#    'not-after': '2020-01-04', # last visible date is 3rd
#    'title': {'en': "Advert", 'fi': "Mainos"},
#    'text': {'en': "We have open positions",
#             'fi': "Meillä on paikkoja"}
#    'href': "https://apluslms.github.io",
#    'image': "https://apluslms.github.io/logo.png",
#}


## Authentication backends
#INSTALLED_APPS += (
#    'shibboleth_login',
#    'social_django',
#)

## Shibboleth options
#SHIBBOLETH_ENVIRONMENT_VARS = {
#    # required for the shibboleth system:
#    'PREFIX': 'SHIB_', # apache2: SHIB_, nginx: HTTP_SHIB_ (NOTE: client can inject HTTP_ vars!)
#    'STUDENT_DOMAIN': 'example.com', # domain where student numbers are selected
#    # ..more options in aplus/settings.py
#}

## Haka
#HAKA_LOGIN = True

## Database
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql',
#        'NAME': 'your_db_name',
#        # use ident auth for local servers
#        # and add passwd&hostname etc for remote
#    }
#}

## Caches
#CACHES = {
#    'default': {
#        # prefer memcached with unix socket
#        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
#        'LOCATION': 'unix:/tmp/memcached.sock',
#
#        # Database cache, if memcached is not possible
#        # remember to run `./manage.py createcachetable`
#        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
#        'LOCATION': 'django_cache_default',
#
#        # Local testing with max size
#        'BACKEND': 'lib.cache.backends.LocMemCache',
#        'LOCATION': 'unique-snowflake',
#        'OPTIONS': {'MAX_SIZE': 1000000}, # simulate memcached value limit
#
#        # or dummy
#        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
#    }
#}

## Sessions
#SESSION_COOKIE_SECURE = True
# Cache-based sessions require the Memcached cache backend.
#SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
# Use browser-length sessions in exam environments so that the A+ session
# cookie is always removed from the browser at the end of the exam.
#SESSION_EXPIRE_AT_BROWSER_CLOSE = True

## Logging
# For debugging purposes
#from .settings import LOGGING
#LOGGING['loggers'].update({
#    '': {
#        'level': 'INFO',
#        'handlers': ['debug_console'],
#        'propagate': True,
#    },
#    'django.db.backends': {
#        'level': 'DEBUG',
#    },
#})
#
## Kubernetes deployment specific settings
# KUBERNETES_MODE = True
# KUBERNETES_NAMESPACE = 'my-k8s-namespace'
