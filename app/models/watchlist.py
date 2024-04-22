from app import db

class WatchlistSymbol(db.Model):
	__tablename__ = "watchlist_symbol"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), unique=True, nullable=False)