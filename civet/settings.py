
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

from __future__ import unicode_literals, absolute_import
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

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

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

# Database used while testing. Just a sqlite DB.
testing_database = {'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
# PostgreSql configuration
postgresql_database = {'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '<db_name>',
        'USER': '<db_username',
        'PASSWORD': '<password>',
        'HOST': 'localhost',
        'PORT': '',
        'CONN_MAX_AGE': 60,
        }

DATABASES = {'default': testing_database}

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

DEFAULT_LOG_LEVEL = "INFO"

rotating_file_handler = {
        'level': DEFAULT_LOG_LEVEL,
        'class': 'logging.handlers.RotatingFileHandler',
        'filename': 'civet.log',
        'maxBytes': 1024*1024*20, # 20M
        'backupCount': 5,
        'formatter': 'simple',
    }

default_file_handler = {
        'level': DEFAULT_LOG_LEVEL,
        'class': 'logging.FileHandler',
        'filename': 'civet.log',
        'formatter': 'simple',
    }

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(asctime)s:%(levelname)s:%(message)s',
            'datefmt': "%Y-%m-%d %H:%M:%S",
        },
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
            'datefmt': "%Y-%m-%d %H:%M:%S",
        },
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[%(server_time)s] %(message)s',
        },
    },
    'handlers': {
        'file': default_file_handler,
        'console': {
            'level': DEFAULT_LOG_LEVEL,
            'class':'logging.StreamHandler',
            'formatter': 'simple',
        },
        'django.server': {
            'level': DEFAULT_LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console', 'file'],
            'level': DEFAULT_LOG_LEVEL,
            'propagate': True,
        },
        'django': {
            'handlers':['console', 'file'],
            'propagate': True,
            'level': DEFAULT_LOG_LEVEL,
        },
        'ci': {
            'handlers':['console', 'file'],
            'propagate': True,
            'level': DEFAULT_LOG_LEVEL,
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': DEFAULT_LOG_LEVEL,
            'propagate': False,
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
    'mooseframework.org',
  )
CORS_ALLOW_METHODS = (
    'GET',
  )

"""
General Git server Options
type[int]: Indicates what type of API to use
api_url[str]: The base URL to access the API
html_url[str]: The base URL for providing links
hostname[str]: Hostname for the configuration. The hostname will
        be matched in the recipes. Ex, in a recipe:
            repository = git@github.com:idaholab/civet
        will match the hostname github.com
secret_id[str]: The secret given by OAuth Apps
client_id[str]: The client id given by OAuth Apps
post_event_summary[bool]: Whether to post a PR comment with a summary of job statuses
post_job_status[bool]: Whether to post a PR comment when a job finishes
remote_update[bool]: flag used while testing. Prevents the update of comments and PR statuses.
install_webhook[bool]: Determines if a webhook is installed when doing
    ./manage.py load_recipes --install-webhooks
remove_pr_label_prefix[list[str]]: Labels with this prefix will be removed when a PR branch is pushed to
pr_wip_prefix[list[str]]: If a PR has a title that starts with one of these then it will be ignored.
failed_but_allowed_label_name[str]: If set, this label will be added to a PR if
        there are failed but allowed tests for a commit.
        Normally the CI status on the GitHub page would
        just show green and it is not obvious that some
        tests have failed.
        This label will be removed automatically when
        new commits are pushed to the PR.
recipe_label_activation[dict]: Labels for dynamic job activation.
        The keys should correspond to "activate_label" on the recipes.
        The values correspond to the files that have changed.
recipe_label_activation_additive[str]: Labels in this list match the keys in recipe_label_activation.
        The difference being that if all the changed files in the PR
        match one of these labels, all the regular tests will run
        in addition to the recipes that match this label.
        If it is not in this list then only recipes matching
        the label (and their dependencies) are run.
ssl_cert[bool]: Setting this to false will cause SSL cert verification
        to be disabled when communicating with the GitLab server.
        Setting it to a filename of the cert of the server will enable
        verification with the added bonus of reducing the number
        of log messages.
authorized_users[list[str]]: These users can see job client information.
        Can contain groups, users, and teams.
        Example: "idaholab/MOOSE Team"
icon_class[str]: This is the CSS class that will be used when showing the server icon.
"""

github_repo_settings = {
        "idaholab/moose":
            {
                "failed_but_allowed_label_name": "PR: Failed but allowed",
                "recipe_label_activation": {
                    "MOOSE_DOCUMENTATION": "^docs/|python/MooseDocs/",
                    "MOOSE_TUTORIAL": "^tutorials/",
                    "MOOSE_EXAMPLES": "^examples/",
                    "MOOSE_PYTHON": "^python/chigger/|python/peacock/|python/mooseutils/",
                },
                "recipe_label_activation_additive": [],
                "branch_settings": {
                    "devel": {
                        "auto_cancel_push_events_except_current": True,
                        "auto_uncancel_previous_event": True,
                    },
                },
                "auto_merge_require_review": True,
                "auto_merge_label": "PR: Auto Merge",
                "auto_merge_do_not_merge_label": "PR: Do Not Merge",
                "auto_merge_enabled": False,
            },
        }

github_config = {"type": GITSERVER_GITHUB,
        "api_url": "https://api.github.com",
        "html_url": "https://github.com",
        "hostname": "github.com",
        "secret_id": "<secret_id>",
        "client_id": "<client_id>",
        "post_event_summary": False,
        "post_job_status": False,
        "remote_update": False,
        "install_webhook": False,
        "remove_pr_label_prefix": ["PR: [TODO]",],
        "pr_wip_prefix": ["WIP:", "[WIP]"],
        "failed_but_allowed_label_name": None,
        "recipe_label_activation": {},
        "recipe_label_activation_additive": [],
        "authorized_users": ['idaholab'],
        "request_timeout": 5,
        "icon_class": "fa fa-github fa-lg",
        "civet_base_url": ABSOLUTE_BASE_URL,
        "repository_settings": github_repo_settings,
    }

gitlab_config = {"type": GITSERVER_GITLAB,
        "api_url": "http://<API_HOSTNAME>",
        "html_url": "http://<API_HOSTNAME>",
        "hostname": "<hostname>",
        "secret_id": "<secret_id>",
        "client_id": "<client_id>",
        "ssl_cert": False,
        "post_event_summary": False,
        "post_job_status": False,
        "remote_update": False,
        "install_webhook": False,
        "pr_wip_prefix": ["WIP:", "[WIP]"],
        "failed_but_allowed_label_name": None,
        "recipe_label_activation": {},
        "recipe_label_activation_additive": [],
        "authorized_users": [],
        "request_timeout": 5,
        "icon_class": "fa fa-gitlab fa-lg",
        "civet_base_url": ABSOLUTE_BASE_URL,
    }

bitbucket_config = {"type": GITSERVER_BITBUCKET,
        "api1_url": "https://bitbucket.org/api/1.0",
        "api2_url": "https://api.bitbucket.org/2.0",
        "html_url": "https://bitbucket.org",
        "hostname": "bitbucket.org",
        "secret_id": "<secret_id>",
        "client_id": "<client_id>",
        "post_event_summary": False,
        "post_job_status": False,
        "remote_update": False,
        "install_webhook": False,
        "recipe_label_activation": {},
        "recipe_label_activation_additive": [],
        "authorized_users": [],
        "request_timeout": 5,
        "icon_class": "fa fa-bitbucket fa-lg",
        "civet_base_url": ABSOLUTE_BASE_URL,
    }

# supported gitservers
INSTALLED_GITSERVERS = [github_config]
