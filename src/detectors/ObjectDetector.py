import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2

class ObjectDetector:
    def __init__(self):
        # Initialize the object detector
        base_options = python.BaseOptions(model_asset_path='models/objects/efficientdet_lite0.tflite')
        options = vision.ObjectDetectorOptions(base_options=base_options, score_threshold=0.5)
        self.detector = vision.ObjectDetector.create_from_options(options)

    def visualize(self, image, detections: list, print_labels=False):
        for detection in detections:
            if print_labels:
                print(f"{detection.categories[0].category_name}: {detection.categories[0].score}")
            # Draw bounding box.
            bbox = detection.bounding_box
            start_point = bbox.origin_x, bbox.origin_y
            end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
            cv2.rectangle(image, start_point, end_point, (255, 0, 0), 2)
        return image
    
    def detect(self, frame, print_labels=False) -> list:
        """ Detect objects in the frame and return a list of detections. """
        # Convert the image to RGB.
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame.
        image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)

        # Detect objects in the frame.
        detections = self.detector.detect(image)

        for detection in detections.detections:
            if print_labels:
                print(f"{detection.categories[0].category_name}: {detection.categories[0].score}")
        return detections.detections

if __name__ == "__main__":
    detector = ObjectDetector()
    
    # Create a video capture object to read frames from the camera.
    cap = cv2.VideoCapture(0)

    # Process each frame.
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        detections = detector.detect(image)
        image = detector.visualize(image, detections)

        # Display the annotated frame.
        cv2.imshow('MediaPipe Object Detection', image)

        if cv2.waitKey(5) & 0xFF == 27:  
            break
    
    # Release resources.
    cap.release()