import ccxt  # noqa: E402

from config import Config, Params
from utils import get_history, send_to_webhook, plot_candles, plot_rsi_macd

cb = ccxt.coinbase({
	'apiKey': Config.CB_API_KEY.value,
	'secret': Config.CB_SECRET_KEY.value,
	'options': {'fetchTicker': 'fetchTickerV3', 'fetchTickers': 'fetchTickersV3'}  # for selecting previous versions
	# 'verbose': True,  # for debug output
})

def lambda_handler():
	for ticker in Params.TICKERS.value:
		# Get the historical data
		history = get_history(cb, ticker, Params.INTERVAL.value, Params.START_DATE.value)
		# Plot the candlestick chart
		ohlcv = plot_candles(history)
		# Plot the RSI and MACD chart
		macd_rsi = plot_rsi_macd(history)
		# Send the plots to Slack
		send_to_webhook(
			f"{ticker}-{Params.START_DATE.value}-{Params.INTERVAL.value}",
			[{'ohlcv': ohlcv}, {'macd_rsi': macd_rsi}],
			Config.WEBHOOK_URL.value
		)

if __name__ == "__main__":
	lambda_handler()
	print("DONE!")
