from threading import Thread
from flask import request
from dotenv import load_dotenv
from app import init_app, logger
from apscheduler.schedulers.background import BackgroundScheduler
## Load environment variables
load_dotenv()

app, socketio, ws, db, itrader = init_app()

with app.app_context():
	db.create_all()

# Initialize APScheduler
scheduler = BackgroundScheduler()
scheduler.add_job(ws.send_price_data, 'interval', seconds=2)
scheduler.start()
 
# Start the itrader thread
itrader_thread = Thread(target=itrader.run)
itrader_thread.start()

# Start streaming data thread
stream_thread = Thread(target=ws.stream_data)
stream_thread.start()


@socketio.on('connect')
def handle_connect():
	client_ip = request.remote_addr
	client_user_agent = request.headers.get('User-Agent')
	logger.info(f'SERVER: Client connected (IP: {client_ip}, User-Agent: {client_user_agent})')


@socketio.on('disconnect')
def handle_disconnect():
	logger.info('SERVER: Client disconnected')

if __name__ == '__main__':
	socketio.run(app, debug=True)