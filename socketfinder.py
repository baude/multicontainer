from pyroute2 import IPDB
import socket
from threading import Thread
from queue import Queue

host = ""

class SocketFinder(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        global host
        while True:
            ip, port = self.queue.get()
            if host == "":
                socket_obj = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                socket.setdefaulttimeout(.1)
                result = socket_obj.connect_ex((ip, port))
                socket_obj.close()
                if result == 0:
                    host = ip
            self.queue.task_done()

def getlocalcidr():
    ip = IPDB()
    foo = ip.interfaces['eth0']
    ipaddy = foo.ipaddr[0]["local"]
    if ipaddy == None:
        ipaddy = foo.ipaddr[1]["local"]
        subnetcidr = foo.ipaddr[1]["prefixlen"]
    else:
        subnetcidr = foo.ipaddr[0]["prefixlen"]
    ip.release()
    return ipaddy, subnetcidr

def findmysqlthreaded(port, ipn):
    global host
    queue = Queue()

    counter = 0
    while host == "":
        if counter == 6:
            break
        for w in range(200):
            worker = SocketFinder(queue)
            worker.daemon = True
            worker.start()
        for i in ipn:
            queue.put(("{}".format(i), port))
        queue.join()
        counter = counter + 1

    return host
