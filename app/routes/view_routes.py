from flask import Blueprint, render_template
from app import wc

views_blueprint = Blueprint('views', __name__)


@views_blueprint.route('/')
def index():
    watchlist = wc.get_all_symbols()
    table_data = [{'symbol': symbol_name, 'price': 0} for symbol_name in watchlist.values()]
	# Example data for the table
    # table_data = [
    #     {'symbol': 'BTCUSD', 'price': '$60,000'},
    #     {'symbol': 'ETHUSD', 'price': '$2,500'},
    # ]
    return render_template('index.html', table_data=table_data)