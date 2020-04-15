# ------------------------------------ log ----------------------------------- #
import logging
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(message)s'))
logger.addHandler(handler)
logger.setLevel(logging.INFO)
# ---------------------------------------------------------------------------- #

from kafka import KafkaConsumer, KafkaProducer
import json

# local module
import s3
import object_detection
from config import KAFKA_HOST, KAFKA_PORT, KAFKA_TOPIC_OBJECT_IMAGE
logger.info("Import complete")

def main():

    logger.info("Setup Kafka Client")
    # Setup Kafka Consumer
    consumer = KafkaConsumer(KAFKA_TOPIC_OBJECT_IMAGE,
                             bootstrap_servers='{}:{}'.format(
                                 KAFKA_HOST, KAFKA_PORT),
                             auto_offset_reset='earliest',
                             enable_auto_commit=True,
                             group_id='object-detection-group')
    # Setup Kafka Producer
    producer = KafkaProducer(
        bootstrap_servers='{}:{}'.format(KAFKA_HOST, KAFKA_PORT))

    logger.info("# Ready for consuming #")

    for message in consumer:
        logger.info("Consume Message")

        # de-serialize
        message_json = json.loads(message.value.decode('utf-8'))
        logger.info(message_json)

        # Get image from S3
        image_stream = s3.get_file_stream(message_json['object_image_path'])

        # detect object in image
        logger.info("detecting...")
        detected_image, detections = object_detection.detect(image_stream)

        logger.info(detections)


# Force to run main()
main()
