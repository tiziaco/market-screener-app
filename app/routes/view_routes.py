from flask import Blueprint, render_template, session, json
from datetime import timedelta
from app import wc, itrader

from itrader.outils.time_parser import get_last_available_timestamp, get_timenow_awere, round_timestamp_to_frequency

views_blueprint = Blueprint('views', __name__)


@views_blueprint.route('/')
def index():
	watchlist = wc.get_all_symbols()
	watchlist_data = [{'symbol': symbol_name, 'price': 0} for symbol_name in watchlist.values()]
	
	# Get screener data
	screener_data = itrader.screeners_handler.to_dict()
	# Get last close price for all symbols
	last_close = {symbol: itrader.price_handler.get_last_close(symbol) for symbol in itrader.price_handler.available_symbols}
	# Get close 24h ago
	now = get_timenow_awere()
	timestamp_24h = now - timedelta(hours=24)
	timestamp_24h = round_timestamp_to_frequency(timestamp_24h, timedelta(hours=1))
	close_24h = {symbol: itrader.price_handler.get_bar(symbol, timestamp_24h).loc['close'] for symbol in itrader.price_handler.available_symbols}

	return render_template('index.html',
						   table_data=watchlist_data,
						   screener_data=screener_data,
						   last_close = json.dumps(last_close),
						   close_24h = json.dumps(close_24h)
						   )