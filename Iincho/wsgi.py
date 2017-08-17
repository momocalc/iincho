"""
WSGI config for Iincho project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
import dotenv

from django.core.wsgi import get_wsgi_application

env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
dotenv.read_dotenv(env_file)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Iincho.settings")

application = get_wsgi_application()
