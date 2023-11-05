import requests
import plotly.io as pio

from config import Params, Config
from utils import upload_to_s3

####################################################################
## Send Images
####################################################################
def send_to_webhook(text, figs, webhook_url):
	urls = []
	for fig_dict in figs:
		for key, value in fig_dict.items():
			# Update the layout of the figure to set a specific width
			value.update_layout(width=int(Params.IMAGE_WIDTH.value))  # Set width to 800 pixels

			# Convert the Plotly graph to a static image
			img_bytes = pio.to_image(value, format='png')

			# Upload the image to S3
			img_url = upload_to_s3(
				img_bytes, key + ".png",
				Config.AWS_S3_BUCKET.value,
				Config.AWS_S3_FILE_PATH.value
			)
			urls.append({"image_url": img_url})

	# Send the image URL via a Slack webhook
	payload = {
		"text": text,
		"attachments": urls
	}
	print(text)
	response = requests.post(
		url=webhook_url,
		json=payload,
		timeout=5
	)

	# Check for errors in the response
	if response.status_code != 200:
		print(f'Error: {response.status_code}, {response.text}')
	else:
		response.raise_for_status()

####################################################################
## Send to Text Webhoook
####################################################################
def send_message_to_slack(text, webhook_url):
	# Make sure the text is not empty
    if not text.strip():
        raise ValueError("The text parameter is empty.")

    # Send the text via a Slack webhook
    payload = {
        "text": text
    }
    try:
        response = requests.post(
            url=webhook_url,
            json=payload,
            headers={'Content-Type': 'application/json'},  # Set the appropriate header
            timeout=5
        )
        response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6+
    except Exception as err:
        print(f'An error occurred: {err}')  # Python 3.6+
    else:
        # If no errors, print the response text
        print('Message sent successfully, response:', response.text)