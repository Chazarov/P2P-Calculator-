import os, sys
sys.path.insert(0, '/home/z/zaharoz0/sibtrust-p2p.ru')
sys.path.insert(1, '/home/z/zaharoz0/sibtrust-p2p.ru/.venv/lib/python3.10/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'P2PCalculator.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()