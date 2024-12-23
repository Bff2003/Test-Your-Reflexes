import pprint
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.framework.formats import landmark_pb2
from mediapipe import solutions
from mediapipe.python.solutions import drawing_styles
import cv2

class HandsDetector:

    # Indexes of the wrist, thumb, and index finger landmarks.
    WRIST_INDEX = 0
    THUMB_INDEX = 4
    INDEX_FINGER_INDEX = 8
    MIDDLE_FINGER_INDEX = 12
    RING_FINGER_INDEX = 16
    PINKY_INDEX = 20

    THUMP_CMC_INDEX = 1
    THUMP_MCP_INDEX = 2
    THUMP_IP_INDEX = 3
    THUMP_TIP_INDEX = 4

    INDEX_FINGER_MCP_INDEX = 5
    INDEX_FINGER_PIP_INDEX = 6
    INDEX_FINGER_DIP_INDEX = 7
    INDEX_FINGER_TIP_INDEX = 8

    MIDDLE_FINGER_MCP_INDEX = 9
    MIDDLE_FINGER_PIP_INDEX = 10
    MIDDLE_FINGER_DIP_INDEX = 11
    MIDDLE_FINGER_TIP_INDEX = 12

    RING_FINGER_MCP_INDEX = 13
    RING_FINGER_PIP_INDEX = 14
    RING_FINGER_DIP_INDEX = 15
    RING_FINGER_TIP_INDEX = 16

    PINKY_MCP_INDEX = 17
    PINKY_PIP_INDEX = 18
    PINKY_DIP_INDEX = 19
    PINKY_TIP_INDEX = 20

    def __init__(self):
        # Initialize the object detector
        base_options = python.BaseOptions(model_asset_path='models/hands/hand_landmarker.task')
        options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=2)
        self.detector = vision.HandLandmarker.create_from_options(options)

    def visualize(self, image, detection_result: list):
        MARGIN = 10  # pixels
        FONT_SIZE = 1
        FONT_THICKNESS = 1
        HANDEDNESS_TEXT_COLOR = (88, 205, 54) # vibrant green

        hand_landmarks_list = detection_result.hand_landmarks
        handedness_list = detection_result.handedness
        annotated_image = np.copy(image)

        # Loop through the detected hands to visualize.
        for idx in range(len(hand_landmarks_list)):
            hand_landmarks = hand_landmarks_list[idx] # Hand landmarks
            handedness = handedness_list[idx] # Left or right hand

            # Draw the hand landmarks.
            hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            hand_landmarks_proto.landmark.extend([
                landmark_pb2.NormalizedLandmark(
                    x=landmark.x, 
                    y=landmark.y, 
                    z=landmark.z
                ) for landmark in hand_landmarks
            ])
            solutions.drawing_utils.draw_landmarks(
                annotated_image,
                hand_landmarks_proto,
                solutions.hands.HAND_CONNECTIONS,
                solutions.drawing_styles.get_default_hand_landmarks_style(),
                solutions.drawing_styles.get_default_hand_connections_style()
            )

            # Get the top left corner of the detected hand's bounding box.
            height, width, _ = annotated_image.shape
            x_coordinates = [landmark.x for landmark in hand_landmarks]
            y_coordinates = [landmark.y for landmark in hand_landmarks]
            text_x = int(min(x_coordinates) * width)
            text_y = int(min(y_coordinates) * height) - MARGIN

            # Draw handedness (left or right hand) on the image.
            cv2.putText(
                annotated_image, 
                f"{handedness[0].category_name}",
                (text_x, text_y), 
                cv2.FONT_HERSHEY_DUPLEX,
                FONT_SIZE, 
                HANDEDNESS_TEXT_COLOR, 
                FONT_THICKNESS, 
                cv2.LINE_AA
            )

        return annotated_image
    
    def detect(self, frame) -> list:
        """ Detect objects in the frame and return a list of detections. """
        # Convert the image to RGB.
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame.
        image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)

        # Detect objects in the frame.
        detections = self.detector.detect(image)

        # for detection in detections.pose_landmarks:
        #     print(detection)
        return detections

if __name__ == "__main__":
    detector = HandsDetector()
    
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