import sys

# local module
import s3
import object_detection
print("Import complete")


def main():
    # Get image from S3
    image_stream = s3.get_file_stream(sys.argv[1])

    # detect object in image
    print("detecting...")
    detected_image, detections = object_detection.detect(image_stream)

    print(detections)


# Force to run main()
main()
