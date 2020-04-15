from imageai.Detection import ObjectDetection

# Setup model
detector = ObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath('yolo.h5')
detector.loadModel()


def detect(image_stream):
    returned_image, detections = detector.detectObjectsFromImage(input_image=image_stream, input_type="stream",
                                                                 output_type="array", minimum_percentage_probability=30)
    return returned_image, detections
