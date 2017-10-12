from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from random import randint
import wiki_search
import json

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def hello_world():
    return render_template('index.html')

@socketio.on('client connected')
def handle_client_connected(json_data):
    print('{0}'.format(str(json_data)))

@socketio.on('search request')
def handle_search_request(json_data):
    print('{0}'.format(str(json_data)))
    wiki_search.add_search_request(json_data)
    goal_wiki_page = wiki_search.find_shortest_path(json_data['start'], json_data['end'])
    shortest_path = wiki_search.get_formatted_shortest_path(goal_wiki_page)
    emit('search response', json.dumps(shortest_path), broadcast=True)

if __name__ == 'main':
    socketio.run(app, host='0.0.0.0')