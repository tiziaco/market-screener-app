import websocket, json
import pandas as pd
import datetime as dt
from queue import Queue
from cachetools import Cache

from itrader.price_handler.data_provider import PriceHandler
from itrader.events_handler.event import PingEvent

from app.utils.time import get_timenow_awere
from app import logger

class BinanceWebsocket():
	"""
	BINANCE_data_provider is designed to download data from the
	BINANCE server. It contains Open-High-Low-Close-Volume (OHLCV) data
	for each pair and streams those to the provided events queue as BarEvents.
	"""
	
	def __init__(self, socketio, price_handler: PriceHandler, global_queue: Queue):
		"""
		Parameters
		----------
		socketio: `SocketIO`
				Web socket connection object.
		"""
		self.socketio = socketio
		self.price_handler = price_handler
		self.global_queue = global_queue
		self.klines_stream = None
		#self.symbols = ['BTCUSDT', 'ETHUSDT']
		self.timeframe = '1m'
		self.websocket = self._initialise_websocket()
		self.is_connected = False
		self.last_tick = Cache(10000)

		self.ticks=0
		self._closed=0
		self._send_ping = False
		logger.info("WEBSOCKET -> OK")


	def send_price_data(self):
		"""
		Send the last price update to the client via Websocket.
		"""
		cache_dict = {key: value for key, value in self.last_tick.items()}
		self.socketio.emit('priceData', cache_dict)

	def stream_data(self):
		"""
		Start to stream the pricedata data from the BINANCE server.
		It streams the klines for a defined timeframe.
		"""
		self._set_klines_stream()
		self.websocket.url = self.klines_stream
		self.websocket.run_forever()
	
	def stop_streaming(self):
		"""
		Close the websocket connection.
		"""
		self.websocket.close()
		logger.info("DATA STREAM: Binance streaming stopped.")
	
	def _initialise_websocket(self):
		"""
		Initialise the websocket object.
		"""
		return websocket.WebSocketApp(self.klines_stream, on_open=self._on_open, on_close=self._on_close,
									on_error=self._on_error, on_message=self._on_message)
	
	def _set_klines_stream(self):
		"""
		Define the complete URL link to connect to the Binance server.
		"""
		klines_stream = 'wss://stream.binance.com:9443/stream?streams='
		
		low = list(map(lambda x: x.lower(), self.price_handler.symbols))
		for sym in low:
			klines_stream += sym+'@kline_'+self.timeframe+'/'
		self.klines_stream = klines_stream[:-1]
	
	def _on_message(self, ws, message):
		"""
		Process the data recived from the websocket.

		Parameters
		----------
		ws: 'websocket'
			Not used
		message: 'str'
			The data package sended from the websocket
		"""
		msg = json.loads(message)['data']
		self.ticks += 1
		# Emit a message with SocketIO for the client
		#self.send_price_data(self.parse_price_dict(msg))
		self._store_tick(msg)
		#print(f'{msg['k']['s']}: {msg['k']['c']}')

		if msg['s'] in self.price_handler.symbols:
			if msg['k']['x']:
				self.ticks = 0
				self._store_bar(msg)
				# TEST:
				self._closed += 1
				self._send_ping = True
				if self._closed == 372:
					#self._closed = 0
					print(f'\n*** BAR CLOSED : M1')
					now = dt.datetime.now()
					print(f'Total closed 1: ' + str(self._closed) + ' ' + dt.datetime.strftime(now, '%Y-%m-%d %H:%M:%S'))
					event = PingEvent(get_timenow_awere())
					self.global_queue.put(event)
			else:
				# Send ping event Method 2
				# Funziona ma troppo lag: devo aspettare il tick successivo la closed bar, troppo tempo.
				if self._send_ping:
					self._send_ping = False
					self.ticks = 0
					print(f'*** BAR CLOSED : M2')
					now = dt.datetime.now()
					print(f'Total closed 2: ' + str(self._closed) + ' '  + dt.datetime.strftime(now, '%Y-%m-%d %H:%M:%S'))
					self._closed = 0

	def _on_open(self, ws):
		"""
		Callback method triggered when the connection is opened
		"""
		self.is_connected = True
		logger.info("DATA STREAM: Binance Websocket connection opened. Data streaming started.")

	def _on_close(self, ws, *kwargs):
		"""
		Callback method triggered when the connection drops
		"""
		logger.info("DATA STREAM: Binance Websocket connection closed")
		self.is_connected = False

	def _on_error(self, ws, msg: str, *kwargs):
		"""
		Callback method triggered in case of error
		:param msg:
		:return:
		"""
		logger.error("DATA STREAM: Binance connection error: %s", msg)
	
	# Data storage
	def _store_bar(self, msg):
		"""
		Store the last completed bar in the prices DataFrame.

		Parameters
		----------
		msg: 'json'
			the data recived from the websocket
		"""
		# Save bar time
		self.time = pd.to_datetime(msg['k']['t'], unit='ms', utc=True).tz_convert('Europe/Paris')
		# Create a dictionary with the completed bar
		bar_dict={self.time :
					{'open': msg['k']['o'],
					'high': msg['k']['h'],
					'low': msg['k']['l'],
					'close': msg['k']['c'],
					'volume':msg['k']['v']
					}
				}
		# Save the ticker who got the data
		self.completed_bars=[]
		self.completed_bars.append(msg['s'])

		# Add the bar in the ticker DataFrame
		df = pd.DataFrame.from_dict(bar_dict, orient='index', dtype=float)

		# Add the bar in the ticker DataFrame
		self.price_handler.prices[msg['s']] = pd.concat([self.price_handler.prices[msg['s']], df])

		# Slice the dataframe to the last max_prices_length bars
		self.price_handler.prices[msg['s']] = self.price_handler.prices[msg['s']].tail(400)

		self.ticks = 0

	def _store_tick(self, msg):
		"""
		Clean, format and store in a dict the data for each symbol present in the WebSocket message
		
		Not used yet.
		"""
		 # Extract relevant data from the message
		symbol = msg.get('s')
		last_price = float(msg.get('k', {}).get('c', 0))  # Default to 0 if price data is not available

		# Store the data in the cache
		self.last_tick[symbol] = last_price

	@staticmethod
	def parse_price_dict(msg: dict):
		return {
			'symbol': str(msg['k']['s']),
			'price' : float(msg['k']['c'])
			}