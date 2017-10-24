import os

SLACK_WEBHOOK = os.environ.get('CHEF_SLACK_WEBHOOK')
SLACK_CHANNEL = os.environ.get('CHEF_SLACK_CHANNEL')
ZOMATO_API_KEY = os.environ.get('CHEF_ZOMATO_API_KEY')
TIME = os.environ.get('CHEF_NOTIFY_AT', '11:00')
