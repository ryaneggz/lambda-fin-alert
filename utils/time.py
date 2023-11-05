import pytz
import datetime


def central_unix_ts(date_time):
	# Create a timezone object for the 'America/Chicago' timezone
	chicago_tz = pytz.timezone('America/Chicago')

	# Parse the date and time string to a datetime object
	dt = datetime.datetime.strptime(date_time, '%m/%d/%Y %I:%M %p')

	# Localize the datetime object to the 'America/Chicago' timezone
	localized_dt = chicago_tz.localize(dt)

	# Convert the localized datetime object to a Unix timestamp
	return int(localized_dt.timestamp()) * 1000

def unix_timestamp_to_string(unix_timestamp, timezone='America/Chicago'):
    # Convert the Unix timestamp to a timezone-aware datetime object
    tz = pytz.timezone(timezone)
    dt = datetime.datetime.fromtimestamp(unix_timestamp, tz)

    # Format the datetime object as a string
    formatted_string = dt.strftime('%m/%d/%Y %I:%M %p')
    return formatted_string