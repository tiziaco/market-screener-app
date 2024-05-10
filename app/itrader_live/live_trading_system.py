import queue
import time
from datetime import datetime

from itrader.events_handler.full_event_handler import EventHandler
from itrader.price_handler.data_provider import PriceHandler
from itrader.strategy_handler.strategies_handler import StrategiesHandler
from itrader.screeners_handler.screeners_handler import ScreenersHandler
from itrader.order_handler.order_handler import OrderHandler
from itrader.portfolio_handler.portfolio_handler import PortfolioHandler
from itrader.execution_handler.execution_handler import ExecutionHandler
from itrader.trading_system.simulation.ping_generator import PingGenerator
from itrader.universe.dynamic import DynamicUniverse
from itrader.reporting.statistics import StatisticsReporting

from itrader import logger
from itrader.events_handler.event import EventType


class TradingSystem(object):
	"""
	Enscapsulates the settings and components for
	carrying out either a backtest session.
	"""
	def __init__(
		self, global_queue: queue.Queue, price_handler: PriceHandler,
		to_sql = False,
	):
		"""
		Set up the backtest variables according to
		what has been passed in.
		"""
		self.to_sql = to_sql
		self.is_running = True

		self.global_queue = global_queue
		self.price_handler = price_handler
		self.universe = DynamicUniverse(self.price_handler, self.global_queue)
		self.strategies_handler = StrategiesHandler(self.global_queue, self.price_handler)
		self.screeners_handler = ScreenersHandler(self.global_queue, self.price_handler)
		self.portfolio_handler = PortfolioHandler(self.global_queue)
		self.order_handler = OrderHandler(self.global_queue)
		self.execution_handler = ExecutionHandler(self.global_queue)
		self.ping = PingGenerator()
		#self.reporting = StatisticsReporting()
		self.event_handler = EventHandler(
			self.strategies_handler,
			self.screeners_handler,
			self.portfolio_handler,
			self.order_handler,
			self.execution_handler,
			self.universe,
			self.global_queue
		)


	def _initialise_live_session(self):
		"""
		Load the data in the price handler and define the pings vector
		for the for-loop iteration.
		"""
		logger.info('TRADING SYSTEM: Initialising backtest session')

		self.universe.init_universe(
			self.strategies_handler.get_strategies_universe(),
			self.screeners_handler.get_screeners_universe())
		self.price_handler.set_symbols(self.universe.get_full_universe())
		self.price_handler.set_timeframe(self.strategies_handler.min_timeframe,
										self.screeners_handler.min_timeframe)
		self.price_handler.load_data()

	def _run_live_session(self):
		"""
		Carries out an for-loop that polls the
		events queue and directs each event to either the
		strategy component of the execution handler. The
		loop continue until the ping series is completed
		"""

		logger.info('SYSTEM |    RUNNING LIVE SESSION')

		while self.is_running:
			if not self.global_queue.empty():
				# Process events if the queue is not empty
				self.event_handler.process_events()
				# Record portfolio metrics
				# self.portfolio_handler.record_portfolios_metrics(ping_event.time)
			else:
				# Sleep for a short interval before checking the queue again
				time.sleep(0.2)
		
		logger.info('SYSTEM |    LIVE SESSION TERMINATED')

	def run(self, print_summary=False):
		"""
		Runs the backtest and print out the backtest statistics
		at the end of the simulation.
		"""
		self._initialise_live_session()
		self._run_live_session()

		# Close the logger file
		#file_handler.close()
		# Close the SQL connection
		#self.sql_engine.dispose() # Close all checked in sessions
