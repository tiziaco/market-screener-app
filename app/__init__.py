from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

#from .websocket.provider import BinanceWebsocket
from .database import db
from app.models.watchlist import WatchlistController

from app.log import init_logger
from app.config import set_config, ENVIRONMENT

config = set_config(ENVIRONMENT)
logger = init_logger(config)

socketio = SocketIO()
#db = SQLAlchemy()
ws = None
wc = None

def init_ws(socketio):
	from .websocket.binance_ws import BinanceWebsocket
	return BinanceWebsocket(socketio)

def init_app():
	global ws
	global socketio
	global db
	global wc

	app = Flask(__name__, template_folder='views')
	app.config.from_object(config)
	db.init_app(app)
	socketio.init_app(app)
	# Init websocket and routes
	with app.app_context():
		ws = init_ws(socketio)
		wc = WatchlistController(db)
		from .routes.view_routes import views_blueprint
		from .routes.api_routes import api_blueprint

		app.register_blueprint(views_blueprint)
		app.register_blueprint(api_blueprint)
	
	return app, socketio, ws, db