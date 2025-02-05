import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask import Flask, Response
from threading import Thread
from cam_inst import VideoCamera
import time

vid = VideoCamera(dev_mode=True)


def init_monitor():
    global vid
    while(True):
        vid.update_frame()


def init_server():
    app.run_server(debug=False, host='0.0.0.0', port=8050)


def gen():
    global vid
    while True:
        time.sleep(0.1)
        frame = vid.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
server = Flask(__name__)
app = dash.Dash(
    __name__, server=server, external_stylesheets=external_stylesheets)


@server.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.callback(Output('live-update-text', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_metrics(n):
    text = vid.__str__()
    style = {'padding': '5px', 'fontSize': '16px'}
    return [html.Span(text, style=style)]


app.title = '东二十'
app.layout = html.Div([
    html.H1("你好！我是东二十"),
    html.Img(src="/video_feed"),
    html.Div([
        html.Div(id='live-update-text'),
        dcc.Interval(
            id='interval-component',
            interval=1*1000  # in milliseconds
        )
    ]),
    html.Div([
            dcc.Markdown('''
            Credit: [Enoch2090](https://github.com/Enoch2090/20)  
            Based on InteliCamPi  
            SJTU 2021
            ''')
        ])
])

if __name__ == '__main__':
    t1 = Thread(target=init_monitor)
    t1.start()
    t2 = Thread(target=init_server)
    t2.start()
    t1.join()
    t2.join()
