from flask import request
from src import app
from flask_socketio import SocketIO
from src.controllers.essay_controller import generate_essay

socketio = SocketIO(app, cors_allowed_origins='*', ping_timeout=120)

@socketio.on('generate-essay')
def generate_essay_event(data):
    generate_essay(socketio, data["user_id"], data["essay"], request.sid)