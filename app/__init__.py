import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from queue import Queue

#from .websocket.provider import BinanceWebsocket
from app.itrader_live import init_itrader
from .database import db
from app.models.watchlist import WatchlistController

from itrader.price_handler.data_provider import PriceHandler

from app.log import init_logger
from app.config import set_config, ENVIRONMENT

config = set_config(ENVIRONMENT)
logger = init_logger(config)

socketio = SocketIO()
#db = SQLAlchemy()
ws = None
wc = None
global_queue = None
itrader = None

def init_ws(socketio, price_handler: PriceHandler, global_queue: Queue):
	from .websocket.binance_ws import BinanceWebsocket
	return BinanceWebsocket(socketio, price_handler, global_queue)

def init_app():
	global ws
	global socketio
	global db
	global wc
	global global_queue
	global itrader

	app = Flask(__name__, template_folder='views')
	# Set a secret key
	app.secret_key = os.urandom(24)
	app.config.from_object(config)
	db.init_app(app)
	socketio.init_app(app)
	global_queue = Queue()
	ph = PriceHandler('binance', ['all'], '5m', '2024-05-06 10:00')
	#ph.load_data()
	itrader = init_itrader(global_queue, ph)
	# Init websocket and routes
	with app.app_context():
		ws = init_ws(socketio, ph, global_queue)
		wc = WatchlistController(db)
		from .routes.view_routes import views_blueprint
		from .routes.api_routes import api_blueprint

		app.register_blueprint(views_blueprint)
		app.register_blueprint(api_blueprint)
	
	return app, socketio, ws, db, itrader