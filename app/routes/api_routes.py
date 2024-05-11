import json
from flask import Response, Blueprint, jsonify, request
from threading import Thread

from app import ws, logger, wc, itrader

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

	added_successfully = wc.add_symbol(name)
	if added_successfully:
		return jsonify({'message': 'Symbol added successfully'}), 200
	else:
		return jsonify({'message': 'Symbol already exists'}), 400

@api_blueprint.route('/watchlist/delete-symbol', methods=['DELETE'])
def watchlist_delete_symbol():
	data = request.get_json()
	symbol_name = data.get('name')
	deleted = wc.delete_symbol(symbol_name)
	if deleted:
		return jsonify({'message': 'SERVER: Symbol deleted successfully'}), 200
	else:
		return jsonify({'message': 'Symbol not found or deletion failed'}), 404

@api_blueprint.route('/watchlist/get-symbols', methods=['GET'])
def watchlist_get_symbols():
	symbol_dict = wc.get_all_symbols()
	return jsonify(symbol_dict), 200

## Screeners routes
@api_blueprint.route('/activate_screener', methods=['POST'])
def activate_screener_route():
    """Activate a screener route"""
    data = request.get_json()
    screener_index = data.get('screener_index')

    if screener_index is None:
        return jsonify({'error': 'Screener index is required'}), 400

    if itrader.screeners_handler.activate_screener(screener_index):
        return jsonify({'message': f'Screener {screener_index} activated'}), 200
    else:
        return jsonify({'error': 'Invalid screener index'}), 400

@api_blueprint.route('/deactivate_screener', methods=['POST'])
def deactivate_screener_route():
    """Deactivate a screener route"""
    data = request.get_json()
    screener_index = data.get('screener_index')

    if screener_index is None:
        return jsonify({'error': 'Screener index is required'}), 400

    if itrader.screeners_handler.deactivate_screener(screener_index):
        return jsonify({'message': f'Screener {screener_index} deactivated'}), 200
    else:
        return jsonify({'error': 'Invalid screener index'}), 400