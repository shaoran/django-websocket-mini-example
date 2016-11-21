"""
WSGI config for websockets project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

import threading
from websockets.thread import WS
obj = WS()
th = threading.Thread(target = obj.listen_and_replay_to_redis)
th.start()


from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "websockets.settings")


application = get_wsgi_application()

# start this with:
# wsgi --socket 127.0.0.1:17999 --wsgi-file websockets/wsgi.py --die-on-term --buffer-size=32768 --workers=5 --master --logto2 /tmp/wsgi_django.log --no-threads-wait --enable-threads
