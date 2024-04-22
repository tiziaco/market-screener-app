from flask import Blueprint, render_template

views_blueprint = Blueprint('views', __name__)


@views_blueprint.route('/')
def index():
	# Example data for the table
    table_data = [
        {'symbol': 'BTCUSD', 'price': '$60,000'},
        {'symbol': 'ETHUSD', 'price': '$2,500'},
    ]
    return render_template('index.html', table_data=table_data)