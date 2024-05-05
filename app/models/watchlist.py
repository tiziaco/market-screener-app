from flask_sqlalchemy import SQLAlchemy

from app import db

class WatchlistSymbol(db.Model):
	__tablename__ = "watchlist_symbol"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), unique=True, nullable=False)

class WatchlistController:
	def __init__(self, db: SQLAlchemy):
		self.db = db
	
	def get_all_symbols(self):
		symbols = WatchlistSymbol.query.all()
		symbol_dict = {int(symbol.id): symbol.name for symbol in symbols}
		return symbol_dict

	def add_symbol(self, name):
		# Check if the symbol already exists in the database
		existing_symbol = WatchlistSymbol.query.filter_by(name=name).first()
		if existing_symbol:
			return False
		
		# Create a new Symbol object
		new_symbol = WatchlistSymbol(name=name)

		# Add the symbol to the database
		self.db.session.add(new_symbol)
		self.db.session.commit()
		return True

	def delete_symbol(self, symbol_name):
		symbol = WatchlistSymbol.query.filter_by(name=symbol_name).first()
		if symbol:
			self.db.session.delete(symbol)
			self.db.session.commit()
			return True
		else:
			return False
