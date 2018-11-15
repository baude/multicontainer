from netaddr import IPNetwork
import random
import time
from db import DBDemo
from socketfinder import getlocalcidr, findmysqlthreaded

port = 3306

if __name__ == '__main__':
    ip, mask = getlocalcidr()
    ipn = IPNetwork("{}/{}".format(ip, mask))
    host = findmysqlthreaded(port, ipn)
    print(host)

    db = DBDemo(host, port)
    db.createtable()

    while True:
        num = random.randint(1, 11)
        print("Sending {}".format(num))
        sql = "INSERT INTO NUMS(NUM) VALUES ('%d')" % (num)
        db.execute(sql)
        db.commit()
        time.sleep(1)

