from .live_trading_system import TradingSystem
from itrader.screeners_handler.screeners.most_performing import MostPerformingScreener

def init_itrader(global_queue, ph):
	itrader = TradingSystem(global_queue, ph)
	# Add screeners
	screener = MostPerformingScreener()
	itrader.screeners_handler.add_screener(screener)
	
	itrader._initialise_live_session()
	return itrader