import ta
import pandas as pd
import plotly.io as pio
import plotly.subplots as sp
import plotly.graph_objects as go

def plot_candles(history, show=False):
	# Convert the data to a Pandas DataFrame
	columns = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
	df = pd.DataFrame(history, columns=columns)

	# Convert the timestamps to the America/Chicago timezone
	df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='ms').dt.tz_localize('UTC').dt.tz_convert('America/Chicago')

	# Create subplots with 2 rows and 1 column, and set the height of the second row (for volume) to be smaller
	fig = sp.make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.7, 0.3], vertical_spacing=0.02)

	# Create the candlestick trace and add it to the first row of subplots
	fig.add_trace(go.Candlestick(x=df['Timestamp'],
					open=df['Open'],
					high=df['High'],
					low=df['Low'],
					close=df['Close']),
					row=1, col=1)

	# Create the volume trace and add it to the second row of subplots
	fig.add_trace(go.Scatter(x=df['Timestamp'], y=df['Volume'], fill='tozeroy', name='Volume'),
					row=2, col=1)

	# Set the layout
	fig.update_layout(
		title='OHLCV Data',
		template='plotly_dark',
		margin=dict(l=10, r=10, t=60, b=40),
		xaxis=dict(
			rangeslider=dict(
				visible=True
			),
			type="date"
		),
	)

	# Update y-axis labels
	fig.update_yaxes(title_text="Price", row=1, col=1)
	fig.update_yaxes(title_text="Volume", row=2, col=1)

	# Show the plot
	if show:
		fig.show()
	return fig

def plot_rsi_macd(history, show=False):
	# Assuming `history` is your data
	columns = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
	df = pd.DataFrame(history, columns=columns)

	# Convert the timestamps to the America/Chicago timezone
	df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='ms').dt.tz_localize('UTC').dt.tz_convert('America/Chicago')

	# Calculate RSI and MACD
	df['RSI'] = ta.momentum.RSIIndicator(df['Close']).rsi()
	macd = ta.trend.MACD(df['Close'])
	df['MACD'] = macd.macd()
	df['MACD Signal'] = macd.macd_signal()

	# Create figure
	fig = go.Figure()

	# Add RSI trace (y-axis on the left)
	fig.add_trace(go.Scatter(x=df['Timestamp'], y=df['RSI'], name='RSI',
							line=dict(width=2, color='yellow')))

	# Add shaded region for RSI
	fig.add_shape(
		type="rect",
		xref="x",
		yref="y",
		x0=df['Timestamp'].min(),
		y0=30,
		x1=df['Timestamp'].max(),
		y1=70,
		fillcolor="darkgrey",
		opacity=0.5,
		layer="below",
		line_width=0,
	)

	# Add MACD and MACD Signal traces (y-axis on the right)
	fig.add_trace(go.Scatter(x=df['Timestamp'], y=df['MACD'], name='MACD',
							line=dict(width=2, color='red'), yaxis='y2'))
	fig.add_trace(go.Scatter(x=df['Timestamp'], y=df['MACD Signal'], name='MACD Signal',
							line=dict(width=2, color='green'), yaxis='y2'))

	# Update layout
	fig.update_layout(
		title='RSI and MACD',
		xaxis=dict(domain=[0, 1]),
		yaxis=dict(title='RSI', titlefont=dict(color='yellow'), tickfont=dict(color='yellow'),
					range=[0, 100], showgrid=False),
		yaxis2=dict(title='MACD', titlefont=dict(color='red'), tickfont=dict(color='red'),
					overlaying='y', side='right', showgrid=False),
		template='plotly_dark',
		margin=dict(l=10, r=10, t=50, b=80),
	)

	# Show the figure
	if show:
		fig.show()
	return fig

def write_to_html_file(fig, file):
	pio.write_html(fig, file)