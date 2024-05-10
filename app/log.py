import os
import logging
from typing import Union


LoggingHandler = Union[logging.StreamHandler, logging.FileHandler]

def init_logger(config):
	print(os.getenv("APP_NAME"))
	logger = logging.getLogger(os.getenv("APP_NAME"))
	logger.setLevel(logging.DEBUG) # Overall minimum logging level
	formatter = logging.Formatter(config.LOGGING_FORMAT)
	
	# Remove old log file
	if os.path.exists('info.log'):
		os.remove('info.log')
	# Minimum logging level for the StreamHandler
	if config.PRINT_LOG:
		stream_handler = logging.StreamHandler()
		stream_handler = set_level(config, stream_handler)
		stream_handler.setFormatter(formatter)
		logger.addHandler(stream_handler)
	if config.SAVE_LOG:
		file_handler = logging.FileHandler('info.log')
		file_handler = set_level(config, stream_handler)
		file_handler.setFormatter(formatter)
		logger.addHandler(file_handler)
	return logger

def set_level(config, handler: LoggingHandler) -> LoggingHandler:
	# Minimum logging level for the StreamHandler
	if config.DEBUG:
		handler.setLevel(logging.DEBUG)
	else:
		handler.setLevel(logging.INFO)
	return handler

