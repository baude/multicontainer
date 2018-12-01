from socketfinder import getlocalcidr, findmysqlthreaded
from db import DBDemo
from netaddr import IPNetwork

from flask import Flask

host = ""
port = 3306
lastid = 1
previousid = 1

out = """<html><head><meta http-equiv="refresh" content="1"></head><body><table><tr><th># Records</th><th>Delta</th></tr><tr><td>{}</td><td>{}</td></tr></table></body></html>
"""


app = Flask(__name__)
@app.route("/")
def hello():
    global lastid, host, previousid
    previousid = lastid
    db = DBDemo(host, port)
    for k, v in db.getresultsfromid(lastid):
        print(k, v)
        lastid = k + 1
    return out.format(lastid, lastid-previousid)


if __name__ == '__main__':
    ip, mask = getlocalcidr()
    print(ip, mask)
    if host == "":
        ipn = IPNetwork("{}/{}".format(ip, mask))
        host = findmysqlthreaded(port, ipn)
        print(host)

    app.run(debug=True, host='0.0.0.0')
