from kafka import KafkaConsumer, KafkaProducer
import json

# local module
import s3
import object_detection
from config import KAFKA_HOST, KAFKA_PORT, KAFKA_TOPIC_OBJECT_IMAGE


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

    print("# Ready for consuming #")

    for message in consumer:
        # de-serialize
        message_json = json.loads(message.value.decode('utf-8'))
        print("message_json", message_json)

        # Get image from S3
        image_stream = s3.get_file_stream(message_json['object_image_path'])

        # detect object in image
        print("detecting...")
        detected_image, detections = object_detection.detect(image_stream)

        print(detections)


if __name__ == '__main__':
    main()
