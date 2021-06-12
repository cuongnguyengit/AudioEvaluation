from flask import Flask, render_template, Response, request, after_this_request, send_from_directory, send_file
# import flask
import sys
# Tornado web server
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
import tornado.ioloop
import os
import time
import argparse


NUM_QUESTION = 6
# Initialize Flask.
app = Flask(__name__)

@app.route('/<path:url>')
def home(url='index.html'):
    return send_from_directory('./', url)

@app.route('/admin/get', methods=['GET'])
def send():
    mem = open('./result.txt', 'rb')
        # mem = rf.read().encode()
    return send_file(
        mem,
        download_name="result.txt",
        as_attachment=True,
        max_age=-1
    )

#
@app.route('/submit', methods=['POST', 'GET'])
def config():
    if request.method == 'GET':
        return render_template('error.html')
    else:
        try:
            result = request.form
            dict_input = {}
            name = dict_input['name'] = result['input_name']
            age = dict_input['age'] = result['input_age']
            region = dict_input['region'] = result['input_region']
            sex = dict_input['sex'] = result['input_sex']
            txt = open('result.txt', 'a', encoding='utf-8')
            for i in range(1, NUM_QUESTION + 1):
                value = result[f'{i}_mos']
                tmp = value.split('_')
                mos = tmp[0]
                path = tmp[-1]
                dict_input[i] = (path, mos)
                txt.write(f'{name}|{age}|{region}|{sex}|{path}|{mos}\n')

            print(dict_input)

            return render_template('thanks.html')
        except Exception as e:
            print(e)
            return render_template('error.html')


# Route to render GUI
@app.route('/')
def show_entries():
    return render_template('index.html', dict_audiotext={
        '01151.wav': 'chưa có gì',
        '02142.wav': 'chưa có',
        '02539.wav': 'chưa gì',
        '13234.wav': 'có gì',
        '13661.wav': 'gì',
        '16152.wav': 'chưa',
    })


# Route to stream music
@app.route('/<voice>', methods=['GET'])
def streammp3(voice):
    def generate():
        with open(os.path.join('./', 'wavs', voice), "rb") as fwav:
            data = fwav.read(1024)
            while data:
                yield data
                data = fwav.read(1024)

    return Response(generate(), mimetype="audio/mp3")

def parse_args(parser):
    """
    Parse commandline arguments.
    """
    parser.add_argument('-p', '--port', type=str, required=True,
                        help='Directory to save checkpoints')
    return parser


# launch a Tornado server with HTTPServer.
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='PyTorch FastPitch Training',
                                     allow_abbrev=False)
    parser = parse_args(parser)
    args, _ = parser.parse_known_args()

    port = args.port
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(port)
    io_loop = tornado.ioloop.IOLoop.current()
    io_loop.start()
