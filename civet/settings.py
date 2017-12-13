
# Copyright 2016 Battelle Energy Alliance, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.conf.locale.en import formats as en_formats
"""
Django settings for civet project.

Generated by 'django-admin startproject' using Django 1.8.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-85d^-^foncz90n+p7ap#irn1&$v*5%d!$u!w0m@w2v*m#&698'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# set to the hosts that urls will have in their names
# In other words, the hosts that this server will accept connections for
# Note that this is required when DEBUG = False
# Ex: ['localhost', 'www.moosebuild.org', 'moosebuild.org']
ALLOWED_HOSTS = []

SHOW_DEBUG_TOOLBAR = False

def show_debug_toolbar(request):
    return DEBUG and SHOW_DEBUG_TOOLBAR

# Make the debug toolbar get a local copy of jquery
DEBUG_TOOLBAR_CONFIG = {"JQUERY_URL": "/static/third_party/jquery-2.1.4/jquery.min.js",
    'SHOW_TOOLBAR_CALLBACK': show_debug_toolbar
    }

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'ci',
    'debug_toolbar',
    'sslserver',
    'graphos',
    'corsheaders',
    'django_extensions',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'civet.urls'

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

WSGI_APPLICATION = 'civet.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql_psycopg2',
#        'NAME': '<db_name>',
#        'USER': 'postgres',
#        'PASSWORD': '<password>',
#        'HOST': 'localhost',
#        'PORT': '',
#        'CONN_MAX_AGE': 60,
#    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
en_formats.DATETIME_FORMAT = 'H:i:s m/d/y e'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

# directory where all the static files go when
# calling ./manage.py collectstatic
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

#DEFAULT_AUTHENTICATION_CLASSES = ( 'rest_framework.authentication.OAuth2Authentication',)
LOGGING = {
  'version': 1,
  'disable_existing_loggers': False,
  'formatters': {
    'simple': {
      'format': '%(asctime)s:%(levelname)s:%(message)s'
    },
    'verbose': {
      'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
    },
  },
  'handlers': {
    'file': {
      'level': 'DEBUG',
      'class': 'logging.FileHandler',
      'filename': 'civet.log',
      'formatter': 'simple',
      },
    'console':{
      'level':'DEBUG',
      'class':'logging.StreamHandler',
      'formatter': 'simple',
      },
    },
    'loggers': {
      'django.request': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
        'propagate': True,
      },
      'django': {
        'handlers':['console', 'file'],
        'propagate': True,
        'level':'INFO',
      },
      'ci': {
        'handlers':['console', 'file'],
        'propagate': True,
        'level':'DEBUG',
      },
    },
  }

#SECURE_CONTENT_TYPE_NOSNIFF=True
#SECURE_BROWSER_XSS_FILTER=True
#SECURE_SSL_REDIRECT=True
#SESSION_COOKIE_SECURE=True
#CSRF_COOKIE_SECURE=True
#CSRF_COOKIE_HTTPONLY=True
#X_FRAME_OPTIONS='DENY'
#SECURE_HSTS_SECONDS=

# location of the recipes directory, relative to the base project directory
RECIPE_BASE_DIR = os.path.join(os.path.dirname(BASE_DIR), 'civet_recipes')

# all the git servers that we support
GITSERVER_GITHUB = 0
GITSERVER_GITLAB = 1
GITSERVER_BITBUCKET = 2

# flag used while testing. Prevents the update of
# comments and PR statuses.
REMOTE_UPDATE = False
# flag used while testing. Prevents installing
# a webhook when a recipe is created.
INSTALL_WEBHOOK = False

# Base URL for this server. This is used in building absolute URLs
# for web hooks on external servers. Ex. https://moosebuild.org
WEBHOOK_BASE_URL = '<URL>'

# supported gitservers
INSTALLED_GITSERVERS = [GITSERVER_GITHUB]

# These users can see job client information.
# Can contain groups, users, and teams.
# Example: "idaholab/MOOSE Team"
AUTHORIZED_USERS = []

# The client and secret given by GitHub
GITHUB_CLIENT_ID = '<client_id>'
GITHUB_SECRET_ID = '<secret_id>'

# Whether to post a PR comment with a summary of job statuses
GITHUB_POST_EVENT_SUMMARY = False
# Whether to post a PR comment when a job finishes
GITHUB_POST_JOB_STATUS = False

# We don't use the client_id/secret on GitLab since
# it doesn't seem to work with LDAP on our internal
# GitLab
GITLAB_API_URL = 'http://<GITLAB_HOSTNAME>'
GITLAB_HOSTNAME = '<hostname>'
# Setting this to false will cause SSL cert verification
# to be disabled when communicating with the GitLab server.
# Setting it to a filename of the cert of the server will enable
# verification with the added bonus of reducing the number
# of log messages.
GITLAB_SSL_CERT = False

# Whether to post a PR comment with a summary of job statuses
GITLAB_POST_EVENT_SUMMARY = False
# Whether to post a PR comment when a job finishes
GITLAB_POST_JOB_STATUS = False

# The client and secret given by BitBucket
BITBUCKET_CLIENT_ID = None
BITBUCKET_SECRET_ID = None

# Whether to post a PR comment with a summary of job statuses
BITBUCKET_POST_EVENT_SUMMARY = False
# Whether to post a PR comment when a job finishes
BITBUCKET_POST_JOB_STATUS = False

# GitHub Labels with this prefix will be removed when a PR branch is pushed to
GITHUB_REMOVE_PR_LABEL_PREFIX = ["PR: [TODO]"]

# If a GitHub PR has a title that starts with one of these then it
# will be ignored.
GITHUB_PR_WIP_PREFIX = ["WIP:", "[WIP]"]

# If a Gitlab PR has a title that starts with one of these then it
# will be ignored.
GITLAB_PR_WIP_PREFIX = ["WIP:", "[WIP]"]

# Instead of checking the Git server each time to check if the
# user is a collaborator on a repo, we cache the results
# for this amount of time. Once this has expired then we
# recheck.
COLLABORATOR_CACHE_TIMEOUT = 60*60

# The absolute url for the server. This is used
# in places where we need to send links to outside
# sources that will point to the server and we
# don't have access to a HttpRequest object.
ABSOLUTE_BASE_URL = "https://localhost"

# Interval (in milliseconds) in which the browser will do an AJAX call to update.
# Put here so that we can dynamically change these while testing
HOME_PAGE_UPDATE_INTERVAL = 20000
JOB_PAGE_UPDATE_INTERVAL = 20000
EVENT_PAGE_UPDATE_INTERVAL = 20000

# This allows for cross origin resource sharing.
# Mainly so that mooseframework.org can have access
# to the mooseframework view.
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = (
    'www.mooseframework.org',
  )
CORS_ALLOW_METHODS = (
    'GET',
  )

# Labels for dynamic job activation.
# The keys should correspond to "activate_label" on the recipes.
# The values correspond to the files that have changed.
RECIPE_LABEL_ACTIVATION = {"MOOSE_DOCUMENTATION": "^docs/|python/MooseDocs/",
    "MOOSE_TUTORIAL": "^tutorials/",
    "MOOSE_EXAMPLES": "^examples/",
    "MOOSE_PYTHON": "^python/chigger/|python/peacock",
    }

# Labels in this list match the keys in RECIPE_LABEL_ACTIVATION.
# The difference being that if all the changed files in the PR
# match one of these labels, all the regular tests will run
# in addition to the recipes that match this label.
# If it is not in this list then only recipes matching
# the label (and their dependencies) are run.
RECIPE_LABEL_ACTIVATION_ADDITIVE = []

# If set, this label will be added to a PR if
# there are failed but allowed tests for a commit.
# Normally the CI status on the GitHub page would
# just show green and it is not obvious that some
# tests have failed.
# This label will be removed automatically when
# new commits are pushed to the PR.
FAILED_BUT_ALLOWED_LABEL_NAME = None
