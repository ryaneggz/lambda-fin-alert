import time
import ccxt  # noqa: E402
import pandas as pd
from ta.trend import MACD
from ta.momentum import RSIIndicator

from config import Config, Params
from utils import get_history, send_to_webhook, plot_candles, plot_rsi_macd, send_message_to_slack, unix_timestamp_to_string

cb = ccxt.coinbase({
	'apiKey': Config.CB_API_KEY.value,
	'secret': Config.CB_SECRET_KEY.value,
	'options': {'fetchTicker': 'fetchTickerV3', 'fetchTickers': 'fetchTickersV3'}  # for selecting previous versions
	# 'verbose': True,  # for debug output
})

def lambda_handler(plot=False, alert=False):
	messages = []
	intervals = Params.INTERVALS.value.split(',')
	for interval in intervals:
		for ticker in Params.TICKERS.value:
			# Get the historical data
			history = get_history(cb, ticker, interval, Params.START_DATE.value)
			# Convert the data to a Pandas DataFrame
			columns = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
			df = pd.DataFrame(history, columns=columns)

			if plot:
				# Plotting functionality...
				if plot:
					ohlcv = plot_candles(history)
					# Plot the RSI and MACD chart
					macd_rsi = plot_rsi_macd(history)
					# Send the plots to Slack
					send_to_webhook(
						f"{ticker}-{Params.START_DATE.value}-{interval}",
						[{'ohlcv': ohlcv}, {'macd_rsi': macd_rsi}],
						Config.WEBHOOK_URL.value
					)

			if alert:
				# Calculate RSI
				rsi_indicator = RSIIndicator(close=df['Close'])
				df['RSI'] = rsi_indicator.rsi()

				# Calculate MACD
				macd_indicator = MACD(close=df['Close'])
				df['MACD_diff'] = macd_indicator.macd_diff()  # MACD difference (MACD line - Signal line)

				# Get the last row of the DataFrame for the latest values
				latest_data = df.iloc[-1]

				# Check for overbought/oversold conditions and MACD difference
				if latest_data['RSI'] > 70 and latest_data['MACD_diff'] > 0:
					messages.append(f"🟥 {ticker} (${latest_data['Close']}) {interval} is overbought with RSI at {round(latest_data['RSI'])} and positive MACD difference at {round(latest_data['MACD_diff'])} potential ⬇️ momentum.")
				elif latest_data['RSI'] < 30 and latest_data['MACD_diff'] < 0:
					messages.append(f"🟩 {ticker} (${latest_data['Close']}) {interval} is oversold with RSI at {round(latest_data['RSI'])} and negative MACD difference at {round(latest_data['MACD_diff'])} potential ⬆️ momentum.")

	if messages:
		current_time_unix = time.time()
		send_message_to_slack(
			unix_timestamp_to_string(current_time_unix) + '\n' + '\n'.join(messages) + '\n',
			Config.WEBHOOK_URL.value
		)

if __name__ == "__main__":
	lambda_handler(alert=True)
	print("DONE!")
