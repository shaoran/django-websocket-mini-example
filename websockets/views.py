from django.shortcuts import render
from django.conf import settings

def index(request):
    return render(request, "index.html")



if settings.DEBUG:
    print "Creating thread for websockets"
    from .thread import WS
    import threading
    obj = WS()
    th = threading.Thread(target = obj.listen_and_replay_to_redis)
    th.start()
