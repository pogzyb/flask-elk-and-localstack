import os

from app import create_app, socketio


if __name__ == "__main__":
    app = create_app('development')
    socketio.run(app, debug=True, host='0.0.0.0', port=int(os.getenv('APP_PORT')))
