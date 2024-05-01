import json
from flask import Response, Blueprint, jsonify, request
from threading import Thread

from app import ws, db, logger, wc
from ..models.watchlist import WatchlistSymbol

api_blueprint = Blueprint('api', __name__)

# *** Websocket routes *** #
@api_blueprint.route('/stop_streaming')
def stop_streaming_route():
	# Check if the streaming process is running
	if ws.is_connected:
		ws.stop_streaming()
		return Response('Streaming stopped', status=200)
	else:
		return Response('Streaming is not running', status=400)

@api_blueprint.route('/start_streaming')
def start_streaming_route():
	# Check if the streaming process is already running
	if not ws.is_connected:
		# Start the streaming process in a new thread
		stream_thread = Thread(target=ws.stream_data)
		stream_thread.start()
		return Response('Streaming started', status=200)
	else:
		return Response('Streaming already in progress', status=400)

# *** Watchlist routes *** #
@api_blueprint.route('/watchlist/add-symbol', methods=['POST'])
def watchlist_add_symbol():
	data = request.get_json()
	name = data.get('name')

	if not name:
		return jsonify({'error': 'Symbol name is required'}), 400

	# Check if the symbol already exists in the database
	existing_symbol = WatchlistSymbol.query.filter_by(name=name).first()
	if existing_symbol:
		return jsonify({'error': 'Symbol already exists'}), 400

	# Create a new Symbol object
	new_symbol = WatchlistSymbol(name=name)

	# Add the symbol to the database
	db.session.add(new_symbol)
	db.session.commit()
	logger.info(f'Watchlist: Symbol added: {name}')
	return Response('Symbol added successfully', status=200)

@api_blueprint.route('/watchlist/delete-symbol/<int:symbol_id>', methods=['DELETE'])
def watchlist_delete_symbol(symbol_id):
	deleted = wc.delete_symbol(symbol_id)
	if deleted:
		return Response('Symbol deleted successfully', status=200, mimetype='application/json')
	else:
		return Response('Symbol not found or deletion failed', status=404, mimetype='application/json')

@api_blueprint.route('/watchlist/get-symbols', methods=['GET'])
def watchlist_get_symbols():
	symbol_dict = wc.get_all_symbols()
	return Response(json.dumps(symbol_dict), status=200, mimetype='application/json')