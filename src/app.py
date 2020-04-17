import json
from kafka import KafkaConsumer, KafkaProducer
import numpy as np 

# local module
import s3
import object_detection
from logger import logger
from config import KAFKA_HOST, KAFKA_PORT, KAFKA_TOPIC_OBJECT_IMAGE, KAFKA_TOPIC_OBJECT_RESULT


# parse numpy object to json
def numpy_default(obj):
    if type(obj).__module__ == np.__name__:
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return obj.item()
    raise TypeError('Unknown type:', type(obj))


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

    logger.info("Ready to receive messages")

    for message in consumer:
        # de-serialize
        message_str = message.value.decode('utf-8')
        message_json = json.loads(message_str)
        logger.info("Input message: %s", message_str)

        # Get image from S3
        image_stream = s3.get_file_stream(message_json['image_path'])

        # detect object in image
        detected_image, detections = object_detection.detect(image_stream)

        # result message
        result = {
            'image_path': message_json['image_path'],
            'detections': detections
        }

        # Send result message
        dumped_result = json.dumps(result, default=numpy_default)
        producer.send(KAFKA_TOPIC_OBJECT_RESULT,
                      value=dumped_result.encode('utf-8'))
        logger.info("Output message: %s", dumped_result)


if __name__ == "__main__":
    main()
