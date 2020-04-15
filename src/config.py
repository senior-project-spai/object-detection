import os

# KAFKA
KAFKA_HOST = os.environ['KAFKA_HOST']
KAFKA_PORT = int(os.environ['KAFKA_PORT'])
KAFKA_TOPIC_OBJECT_IMAGE = os.environ['KAFKA_TOPIC_OBJECT_IMAGE']

# S3
S3_ENDPOINT = os.environ['S3_ENDPOINT']
S3_ACCESS_KEY = os.environ['S3_ACCESS_KEY']
S3_SECRET_KEY = os.environ['S3_SECRET_KEY']