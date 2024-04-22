import websocket, json

from app import logger

class BinanceWebsocket():
	"""
	BINANCE_data_provider is designed to download data from the
	BINANCE server. It contains Open-High-Low-Close-Volume (OHLCV) data
	for each pair and streams those to the provided events queue as BarEvents.
	"""
	
	def __init__(self, socketio):
		"""
		Parameters
		----------
		socketio: `SocketIO`
				Web socket connection object.
		"""

		self.klines_stream = None
		self.symbols = ['BTCUSDT', 'ETHUSDT']
		self.timeframe = '1m'
		self.websocket = self._initialise_websocket()
		self.socketio = socketio
		self.is_connected = False
		self.ticks=0
		logger.info("WEBSOCKET -> OK")


	def send_price_data(self, data):
		"""
		Send the last price update to the client via Websocket.
		"""
		self.socketio.emit('priceData', data)

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
		
		low = list(map(lambda x: x.lower(), self.symbols))
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
		self.send_price_data(self.parse_price_dict(msg))
		#print(f'{msg['k']['s']}: {msg['k']['c']}')

		if msg['s'] in self.symbols:
			if msg['k']['x']:
				self.ticks = 0
				print(f'*** BAR CLOSED : {msg['k']['s']}')

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

	@staticmethod
	def parse_price_dict(msg: dict):
		return {
			'symbol': str(msg['k']['s']),
			'price' : float(msg['k']['c'])
			}