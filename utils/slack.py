import requests
import plotly.io as pio

from config import Params, Config
from utils import upload_to_s3

####################################################################
## Send to Slack Webhoook
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
		json=payload
	)

	# Check for errors in the response
	if response.status_code != 200:
		print(f'Error: {response.status_code}, {response.text}')
	else:
		response.raise_for_status()