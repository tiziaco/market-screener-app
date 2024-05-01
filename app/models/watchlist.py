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
		symbol = WatchlistSymbol(name=name)
		self.db.session.add(symbol)
		self.db.session.commit()

	def delete_symbol(self, symbol_id):
		symbol = WatchlistSymbol.query.get(symbol_id)
		if symbol:
			self.db.session.delete(symbol)
			self.db.session.commit()
			return True
		else:
			return False
