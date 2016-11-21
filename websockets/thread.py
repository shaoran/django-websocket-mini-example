# creating the thread
import socket
import threading
import time
import uuid
import random
import logging

from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage

from datetime import datetime


class WS(object):
    def __init__(self):
        self.counter = 0

    def listen_and_replay_to_redis(self):

        logger = logging.getLogger("django")

        tid = random.randint(1, 1000)
        logger.debug(" >> [%s] websocket starting thread" % tid)


        try:

            redis_publisher = RedisPublisher(facility='foobar', broadcast=True)

            while True:
                data = str(uuid.uuid4())

                #self.counter += 1

                #data = "%s - %s" % (data, self.counter)

                redis_publisher.publish_message(RedisMessage(data))
                ttw = random.uniform(3, 10)
                logger.debug(" >> [%s] websocket thread %s: %s waiting %s seconds" % (tid, datetime.now().strftime("%H:%M:%S"), data, ttw))
                time.sleep(ttw)
        except Exception as e:
            logger.debug(" >> [%s] websocket thread error: %s" % (tid,e))

        logger.debug(" >> [%s] websocket thread dying" % tid)

def old_listen_and_replay_to_redis():
    TCP_IP = '127.0.0.1'
    TCP_PORT = 5555
    BUFFER_SIZE = 1024

    redis_publisher = RedisPublisher(facility='foobar', broadcast=True)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)

    while True:
        conn, addr = s.accept()

        print 'Connection address:', addr

        data = conn.recv(BUFFER_SIZE)
        if not data:
            continue

        try:
            redis_publisher.publish_message(RedisMessage(data))
        except Exception as e:
            print "could not publish in redis because %s" % e

        conn.send("Thank you for your message. Bye.\n")
        conn.close()

#obj = WS()
#th = threading.Thread(target = obj.listen_and_replay_to_redis)

from django.conf import settings

def startup():
    from .wsgi import MYTHREAD
    #obj = WS()
    #th = threading.Thread(target = obj.listen_and_replay_to_redis)

    logger = logging.getLogger("django")

    th = MYTHREAD
    logger.debug("th.is_alive(): %s" % th.is_alive())
    if th.is_alive():
        return
    th.start()
