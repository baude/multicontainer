import dash
from dash.dependencies import Output, Event
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque
from socketfinder import getlocalcidr, findmysqlthreaded
from db import DBDemo
from netaddr import IPNetwork


#class Config(object):
#    def __init__(self, host, port, db, lastid):
#        self.host = host
#        self.port = port
#        self.db = db
#        self.lastid = lastid

host = ""
port = 3306
lastid = 1
X = deque(maxlen=20)
X.append(1)
Y = deque(maxlen=20)
Y.append(1)


app = dash.Dash(__name__)
app.layout = html.Div(
    [
        dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(
            id='graph-update',
            interval=1*1000
        ),
    ]
)

@app.callback(Output('live-graph', 'figure'),
              events=[Event('graph-update', 'interval')])
def update_graph_scatter():
    db = DBDemo(host, port)
    global lastid
    for k, v in db.getresultsfromid(lastid):
        print(k, v)
        lastid = k + 1
        X.append(k)
        Y.append(v)

    #X.append(X[-1]+1)
    #Y.append(Y[-1]+Y[-1]*random.uniform(-0.1,0.1))
    data = plotly.graph_objs.Scatter(
            x=list(X),
            y=list(Y),
            name='Scatter',
            mode= 'lines+markers'
            )

    return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),
                                                yaxis=dict(range=[min(Y),max(Y)]),)}


if __name__ == '__main__':
    ip, mask = getlocalcidr()
    print(ip, mask)
    if host == "":
        ipn = IPNetwork("{}/{}".format(ip, mask))
        host = findmysqlthreaded(port, ipn)
        print(host)

    app.run_server(host=ip)
