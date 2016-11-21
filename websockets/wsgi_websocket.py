import os
import gevent.socket
import redis.connection

redis.connection.socket = gevent.socket

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "websockets.settings")

from ws4redis.uwsgi_runserver import uWSGIWebsocketServer
application = uWSGIWebsocketServer()

# start this with
# uwsgi --socket 127.0.0.1:18000 --wsgi-file websockets/wsgi_websocket.py --die-on-term --gevent 1000 --http-websockets --workers=2 --master --logto2 /tmp/wsgi_websocket.log -b 32768 --protocol=http
