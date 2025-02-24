import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import math
from typing import Tuple, Union

class FaceDetector:
    def __init__(self):
        # Initialize the object detector
        base_options = python.BaseOptions(model_asset_path='models/faces/blaze_face_short_range.tflite')
        options = vision.FaceDetectorOptions(base_options=base_options)
        self.detector = vision.FaceDetector.create_from_options(options)

    def _normalized_to_pixel_coordinates(self, normalized_x: float, normalized_y: float, image_width: int, image_height: int) -> Union[None, Tuple[int, int]]:
        """Converts normalized value pair to pixel coordinates."""

        # Checks if the float value is between 0 and 1.
        def is_valid_normalized_value(value: float) -> bool:
            return (value > 0 or math.isclose(0, value)) and (value < 1 or math.isclose(1, value))

        if not (is_valid_normalized_value(normalized_x) and
                is_valid_normalized_value(normalized_y)):
            return None
        x_px = min(math.floor(normalized_x * image_width), image_width - 1)
        y_px = min(math.floor(normalized_y * image_height), image_height - 1)
        return x_px, y_px

    def visualize(self, image, detections: list):
        for detection in detections:
            print(f"{detection.categories[0].category_name}: {detection.categories[0].score}")
            # Draw bounding_box
            bbox = detection.bounding_box
            start_point = bbox.origin_x, bbox.origin_y
            end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
            cv2.rectangle(image, start_point, end_point, (255, 0, 0), 2)

            # Draw keypoints
            for keypoint in detection.keypoints:
                keypoint_px = self._normalized_to_pixel_coordinates(keypoint.x, keypoint.y, image.shape[1], image.shape[0])
                if keypoint_px:
                    cv2.circle(image, keypoint_px, 2, (0, 255, 0), 2)

        return image

    def detect(self, frame) -> list:
        """ Detect objects in the frame and return a list of detections. """
        # Convert the image to RGB.
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame.
        image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)

        # Detect objects in the frame.
        detections = self.detector.detect(image)

        # for detection in detections.detections:
        #     print(f"{detection.categories[0].category_name}: {detection.categories[0].score}")
        return detections.detections

if __name__ == "__main__":
    detector = FaceDetector()
    
    # Create a video capture object to read frames from the camera.
    cap = cv2.VideoCapture(0)

    # Process each frame.
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        detections = detector.detect(image)
        image = detector.visualize_mask(image, detections, emoji_path="assets/smile.png", scale=1.5)

        # Display the annotated frame.
        cv2.imshow('MediaPipe Object Detection', image)

        if cv2.waitKey(5) & 0xFF == 27:  
            break
    
    # Release resources.
    cap.release()