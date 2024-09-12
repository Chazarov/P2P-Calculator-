# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, '/home/z/zaharoz0/zaharoz0.beget.tech/P2PCalculator')
sys.path.insert(1, '/home/z/zaharoz0/zaharoz0.beget.tech/.venv/lib/python3.10/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'P2PCalculator.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()