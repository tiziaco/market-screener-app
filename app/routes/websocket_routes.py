from flask import request

from app import socketio, logger

@socketio.on('connect')
def handle_connect():
	client_ip = request.remote_addr
	client_user_agent = request.headers.get('User-Agent')
	logger.info(f'SERVER: Client connected (IP: {client_ip}, User-Agent: {client_user_agent})')

@socketio.on('disconnect')
def handle_disconnect():
	logger.info('SERVER: Client disconnected')