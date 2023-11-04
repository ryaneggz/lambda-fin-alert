import ccxt

from .time import central_unix_ts

def get_latest(exchange, symbols):
	try:
		tickers = exchange.fetch_tickers(symbols)
		return tickers
	except (ccxt.RequestTimeout, ccxt.DDoSProtection, ccxt.ExchangeNotAvailable, ccxt.AuthenticationError, ccxt.ExchangeError) as err:
		print(err)

def get_balance(exchange):
	balances = exchange.fetch_balance()
	positive_balances = {k: v for k, v in balances['total'].items() if v != 0}
	return positive_balances

def get_history(exchange, symbol, timeframe, since=None, limit=None):
	try:
		# Max 300 Candles
		candles = exchange.fetch_ohlcv(symbol, timeframe, central_unix_ts(since), limit)
		return candles
	except (ccxt.RequestTimeout, ccxt.DDoSProtection, ccxt.ExchangeNotAvailable, ccxt.AuthenticationError, ccxt.ExchangeError) as err:
		print(err)
