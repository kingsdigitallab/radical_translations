"""
Base settings to build other settings files upon.
"""

import os

import environ

from controlled_vocabulary import defaults

ROOT_DIR = (
    environ.Path(__file__) - 3
)  # (radical_translations/config/settings/base.py - 3 = radical_translations/)
APPS_DIR = ROOT_DIR.path("radical_translations")

env = environ.Env()

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(ROOT_DIR.path(".env")))

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)
# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = "Europe/London"
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = "en-gb"
# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
# https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
LOCALE_PATHS = [ROOT_DIR.path("locale")]

# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {"default": env.db("DATABASE_URL")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = "config.urls"
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "config.wsgi.application"

# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # "django.contrib.humanize", # Handy template tags
    "django.contrib.admin",
]
THIRD_PARTY_APPS = [
    "crispy_forms",
    "rest_framework",
    "wagtail.contrib.forms",
    "wagtail.contrib.modeladmin",
    "wagtail.contrib.routable_page",
    "wagtail.contrib.redirects",
    "wagtail.contrib.settings",
    "wagtail.contrib.table_block",
    "wagtail.search",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.admin",
    "wagtail.core",
    "modelcluster",
    "taggit",
    "kdl_wagtail.core",
    "kdl_wagtail.people",
    "kdl_wagtail.zotero",
    "wagtailmenus",
    "controlled_vocabulary",
    "geonames_place.apps.GeonamesPlaceConfig",
    "polymorphic",
    "django_elasticsearch_dsl",
    "django_elasticsearch_dsl_drf",
    "markdownx",
]

LOCAL_APPS = [
    "radical_translations.users.apps.UsersConfig",
    "radical_translations.utils.apps.UtilsConfig",
    # Your stuff: custom apps go here
    "radical_translations.agents.apps.AgentsConfig",
    "radical_translations.cms.apps.CmsConfig",
    "radical_translations.core.apps.CoreConfig",
    "radical_translations.events.apps.EventsConfig",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIGRATIONS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#migration-modules
MIGRATION_MODULES = {"sites": "radical_translations.contrib.sites.migrations"}

# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = "users.User"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = "users:redirect"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
LOGIN_URL = "account_login"

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation"
        ".UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# MIDDLEWARE
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

# STATIC
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR("staticfiles"))
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = "/static/"
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [str(APPS_DIR.path("static")), str(ROOT_DIR.path("node_modules"))]
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR("media"))
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "/media/"

if not os.path.exists(MEDIA_ROOT):
    os.makedirs(MEDIA_ROOT)

DATA_ROOT = os.path.join(ROOT_DIR, "data")
EXPORTS_ROOT = os.path.join(MEDIA_ROOT, "exports")

if not os.path.exists(EXPORTS_ROOT):
    os.makedirs(EXPORTS_ROOT)


# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        "DIRS": [
            str(APPS_DIR.path("templates")),
            str(APPS_DIR.path("static/fontawesome")),
        ],
        "OPTIONS": {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "radical_translations.utils.context_processors.settings_context",
                "wagtail.contrib.settings.context_processors.settings",
                "wagtailmenus.context_processors.wagtailmenus",
            ],
        },
    }
]
# http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = "bootstrap4"

# FIXTURES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
FIXTURE_DIRS = (str(APPS_DIR.path("fixtures")),)

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-browser-xss-filter
SECURE_BROWSER_XSS_FILTER = True
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = "DENY"

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend"
)
# https://docs.djangoproject.com/en/2.2/ref/settings/#email-timeout
EMAIL_TIMEOUT = 5

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = "admin/"
# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [("""King's Digital Lab""", "k9x5b5t8u6g2x7e9@kingsdigitallab.slack.com")]
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# LOGGING
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}

# Elasticsearch
# ------------------------------------------------------------------------------
# https://github.com/django-es/django-elasticsearch-dsl
ELASTICSEARCH_DSL = {"default": {"hosts": f"{env('ELASTICSEARCH_HOST')}"}}

ES_FACET_OPTIONS = {"order": {"_key": "asc"}, "size": 1000}
ES_FUZZINESS_OPTIONS = {"fuzziness": "1"}

# Wagtail
# ------------------------------------------------------------------------------
# https://docs.wagtail.io/en/v2.7.1/getting_started/integrating_into_django.html
WAGTAIL_SITE_NAME = "Radical Translations"

HOMEPAGE_RICHTEXT_FEATURES = ["bold", "italic", "link"]
HOMEPAGE_SECTION_BLOCK_COUNTS = {"min_number": 4, "max_num": 4}

WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.db",
    }
}

# Your stuff...
# ------------------------------------------------------------------------------

# django-controlled-vocabulary
# ------------------------------------------------------------------------------
# https://github.com/kingsdigitallab/django-controlled-vocabulary#enabling-specific-vocabulary-plug-ins-optional
CONTROLLED_VOCABULARY_VOCABULARIES = defaults.CONTROLLED_VOCABULARY_VOCABULARIES + [
    "radical_translations.core.vocabularies",
]

# django-geonames-place
# https://github.com/kingsdigitallab/django-geonames-place
# ------------------------------------------------------------------------------
GEONAMES_KEY = env("GEONAMES_KEY")
GEONAMES_MAX_RESULTS = 3

# django-kdl-wagtail
# https://github.com/kingsdigitallab/django-kdl-wagtail
# ------------------------------------------------------------------------------
KDL_WAGTAIL_ZOTERO_COLLECTION = env("KDL_WAGTAIL_ZOTERO_COLLECTION", default="")
KDL_WAGTAIL_ZOTERO_LIBRARY_ID = env("KDL_WAGTAIL_ZOTERO_LIBRARY_ID", default="")
KDL_WAGTAIL_ZOTERO_LIBRARY_TYPE = "group"
KDL_WAGTAIL_ZOTERO_NOTE_STYLE = "chicago-fullnote-bibliography"
KDL_WAGTAIL_ZOTERO_SHORTNOTE_STYLE = "chicago-note-bibliography"
KDL_WAGTAIL_ZOTERO_TOKEN = env("KDL_WAGTAIL_ZOTERO_TOKEN", default="")


# django-rest-framework
# https://github.com/encode/django-rest-framework
# ------------------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 50,
    "ORDERING_PARAM": "ordering",
}


# Search
# ------------------------------------------------------------------------------
CONTRIBUTION_MAIN_ROLES = ["author", "translator"]

CONTRIBUTION_OTHER_ROLES = [
    "journalist",
    "editor",
    "publisher",
    "bookseller",
]

SEARCH_OPTIONS = {
    "resources": {
        "label": "Resources",
        "page_size": 50,
        "meta_facets": ["meta"],
        "range_facets": ["year"],
        "year_min": 1516,
        "year_max": 1900,
        "map_field": "places",
        "ordering": [
            {"key": "score", "value": "Relevance"},
            {"key": "title", "value": "Title ascending"},
            {"key": "-title", "value": "Title descending"},
            {"key": "year", "value": "Year ascending"},
            {"key": "-year", "value": "Year descending"},
        ],
    },
    "events": {
        "label": "Events",
        "page_size": 500,
        "meta_facets": [],
        "range_facets": ["year"],
        "year_min": 1780,
        "year_max": 1820,
        "resources": 1,
    },
    "agents": {
        "label": "Agents",
        "page_size": 50,
        "meta_facets": ["meta"],
        "range_facets": ["year"],
        "year_min": 1450,
        "year_max": 1900,
        "map_field": "based_near",
        "filters": [["anonymous", "no"]],
        "ordering": [
            {"key": "score", "value": "Relevance"},
            {"key": "name", "value": "Name ascending"},
            {"key": "-name", "value": "Name descending"},
            {"key": "year", "value": "Year ascending"},
            {"key": "-year", "value": "Year descending"},
        ],
    },
}

# Export
# ------------------------------------------------------------------------------
EXPORT_FIELD_SEPARATOR = "::"
EXPORT_MULTIVALUE_SEPARATOR = ";"
