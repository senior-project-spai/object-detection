import logging
from kafka import KafkaConsumer, KafkaProducer
import json

# local module
import s3
import object_detection
from config import KAFKA_HOST, KAFKA_PORT, KAFKA_TOPIC_OBJECT_IMAGE, KAFKA_TOPIC_OBJECT_RESULT

# Setup root logger
logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.INFO)


def main():
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

    logging.info("Ready to receive messages")

    for message in consumer:
        # de-serialize
        message_str = message.value.decode('utf-8')
        message_json = json.loads(message_str)
        logging.info("Input message: %s", message_str)

        # Get image from S3
        image_stream = s3.get_file_stream(message_json['image_path'])

        # detect object in image
        detected_image, detections = object_detection.detect(image_stream)

        # message
        result = {
            'image_path': message_json['image_path'],
            'detections': detections
        }

        # Send message
        # producer.send(KAFKA_TOPIC_OBJECT_RESULT,
        #               value=json.dumps(result).encode('utf-8'))
        logging.info("Output message: %s", result)


if __name__ == "__main__":
    main()
