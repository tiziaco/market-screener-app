import os
from threading import Thread
from flask import request
from dotenv import load_dotenv
from app import init_app, logger

## Load environment variables
load_dotenv()

app, socketio, ws, db = init_app()

with app.app_context():
	db.create_all()

@socketio.on('connect')
def handle_connect():
	client_ip = request.remote_addr
	client_user_agent = request.headers.get('User-Agent')
	logger.info(f'SERVER: Client connected (IP: {client_ip}, User-Agent: {client_user_agent})')


@socketio.on('disconnect')
def handle_disconnect():
	logger.info('SERVER: Client disconnected')

if __name__ == '__main__':
	stream_thread = Thread(target=ws.stream_data)
	stream_thread.start()

	socketio.run(app, debug=True)