DEBUG = True
############################
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # Full path to database file.  Always use forward slashes even in Windows
        'NAME': os.path.join(BASE_DIR, 'work_local','sqlite3.db'),
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Not used with sqlite3.
        'PORT': '',                      # Not used with sqlite3.
    }
}

LOGGING['handlers']['file']['filename'] = os.path.join(BASE_DIR, 'work_local','spark_debug.log')

# For the Django debug toolbar
#INTERNAL_IPS = ('127.0.0.1',)
