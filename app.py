from src import config, app
from src.services.socketio_service import socketio
from src.services.scheduler_service import scheduler

if __name__ == "__main__":
    scheduler.start()
    socketio.run(app, host=config.HOST, port=config.PORT, debug=config.DEBUG, use_reloader=config.USE_RELOADER)