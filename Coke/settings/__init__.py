import os
from .base import *  # noqa

# Load development settings based on DJANGO_MODE environment variable
if os.environ.get('DJANGO_MODE', 'PRODUCTION') == 'DEVELOPMENT':
    from .development import *
else:
    from .production import *

try:
    from .local import *
except ImportError:
    pass
