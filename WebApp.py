from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from random import randint

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def hello_world():
    return render_template('index.html')

@socketio.on('client connected')
def handle_client_connected(json):
    print('{0}'.format(str(json)))

@socketio.on('search request')
def handle_search_request(json):
    print('{0}'.format(str(json)))
    emit('search response', randint(0,9),broadcast=True)
    emit('search response', randint(0,9),broadcast=True)

if __name__ == 'main':
    socketio.run(app, host='0.0.0.0')