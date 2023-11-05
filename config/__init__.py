import os
from enum import Enum

class Config(Enum):
	"""Config Enum"""
	AWS_S3_FILE_PATH = os.environ.get('AWS_S3_FILE_PATH', 'crypto')
	AWS_S3_REGION = os.environ.get('AWS_S3_REGION', 'us-east-2')
	AWS_S3_BUCKET = os.environ.get('AWS_S3_BUCKET')
	AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
	AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
	WEBHOOK_URL = os.environ.get('WEBHOOK_URL')
	CB_API_KEY = os.environ.get('CB_API_KEY')
	CB_SECRET_KEY = os.environ.get('CB_SECRET_KEY')


class Params(Enum):
	"""Params Enum"""
	IMAGE_WIDTH = os.environ.get('IMAGE_WIDTH', 1500)
	TICKERS = os.environ.get('TICKERS', 'BTC/USD,ETH/USD').split(',')
	START_DATE = os.environ.get('START_DATE')
	INTERVALS = os.environ.get('INTERVALS', '1d')
