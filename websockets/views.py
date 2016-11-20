from django.shortcuts import render

def index(request):
    return render(request, "index.html")




# creating the thread
import socket
import threading
import time
import uuid
import random

from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage


print "Creating thread the listens on port 5555"

class WS(object):
    def __init__(self):
        self.counter = 0

    def listen_and_replay_to_redis(self):

        redis_publisher = RedisPublisher(facility='foobar', broadcast=True)

        while True:
            data = str(uuid.uuid4())

            #self.counter += 1

            #data = "%s - %s" % (data, self.counter)

            redis_publisher.publish_message(RedisMessage(data))
            time.sleep(random.uniform(3, 10))

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


obj = WS()
th = threading.Thread(target = obj.listen_and_replay_to_redis)

th.start()

