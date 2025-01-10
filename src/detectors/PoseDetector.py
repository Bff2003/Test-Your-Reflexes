import pprint
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.framework.formats import landmark_pb2
from mediapipe import solutions
from mediapipe.python.solutions import drawing_styles
import cv2

class PoseDetector:
    NOSE_INDEX = 0
    LEFT_EYE_INNER_INDEX = 1
    LEFT_EYE_INDEX = 2
    LEFT_EYE_OUTER_INDEX = 3
    RIGHT_EYE_INNER_INDEX = 4
    RIGHT_EYE_INDEX = 5
    RIGHT_EYE_OUTER_INDEX = 6
    LEFT_EAR_INDEX = 7
    RIGHT_EAR_INDEX = 8
    MOUTH_LEFT_INDEX = 9
    MOUTH_RIGHT_INDEX = 10
    LEFT_SHOULDER_INDEX = 11
    RIGHT_SHOULDER_INDEX = 12
    LEFT_ELBOW_INDEX = 13
    RIGHT_ELBOW_INDEX = 14
    LEFT_WRIST_INDEX = 15
    RIGHT_WRIST_INDEX = 16
    LEFT_PINKY_INDEX = 17
    RIGHT_PINKY_INDEX = 18
    LEFT_INDEX = 19
    RIGHT_INDEX = 20
    LEFT_THUMB_INDEX = 21
    RIGHT_THUMB_INDEX = 22
    LEFT_HIP_INDEX = 23
    RIGHT_HIP_INDEX = 24
    LEFT_KNEE_INDEX = 25
    RIGHT_KNEE_INDEX = 26
    LEFT_ANKLE_INDEX = 27
    RIGHT_ANKLE_INDEX = 28
    LEFT_HEEL_INDEX = 29
    RIGHT_HEEL_INDEX = 30
    LEFT_FOOT_INDEX = 31
    RIGHT_FOOT_INDEX = 32

    def __init__(self):
        # Initialize the object detector
        base_options = python.BaseOptions(model_asset_path='models/poses/pose_landmarker_heavy.task')
        options = vision.PoseLandmarkerOptions(base_options=base_options, output_segmentation_masks=True)
        self.detector = vision.PoseLandmarker.create_from_options(options)

    def visualize(self, image, detections: list):
        pose_landmarks_list = detections.pose_landmarks
        annotated_image = np.copy(image)

        # Loop through the detected poses to visualize.
        for idx in range(len(pose_landmarks_list)):
            pose_landmarks = pose_landmarks_list[idx]

            # Draw the pose landmarks.
            pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            pose_landmarks_proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in pose_landmarks
            ])
            solutions.drawing_utils.draw_landmarks(
            annotated_image,
            pose_landmarks_proto,
            solutions.pose.POSE_CONNECTIONS,
            solutions.drawing_styles.get_default_pose_landmarks_style())
        return annotated_image
    
    def _add_mask(self, image, landmark, emoji_path, scale=1.0):
        """Add a mask (emoji) to a specific landmark on the pose."""
        # Load the emoji image with alpha channel
        emoji = cv2.imread(emoji_path, cv2.IMREAD_UNCHANGED)
        if emoji is None:
            print(f"Error: Unable to load emoji from {emoji_path}")
            return

        # Get image dimensions
        image_height, image_width, _ = image.shape

        # Convert normalized coordinates to pixel coordinates
        x_px = int(landmark.x * image_width)
        y_px = int(landmark.y * image_height)

        # Resize the emoji to fit a reasonable size around the landmark
        emoji_height, emoji_width = emoji.shape[:2]
        target_width = int(image_width * 0.1 * scale)  # 10% da largura da imagem, ajustável
        target_height = int(emoji_height * (target_width / emoji_width))
        emoji_resized = cv2.resize(emoji, (target_width, target_height), interpolation=cv2.INTER_AREA)

        # Calculate top-left corner for overlay
        x_start = max(0, x_px - target_width // 2)
        y_start = max(0, y_px - target_height // 2)

        # Overlay the emoji on the image
        for i in range(target_height):
            for j in range(target_width):
                if y_start + i >= image.shape[0] or x_start + j >= image.shape[1]:
                    continue
                alpha = emoji_resized[i, j, 3] / 255.0  # Alpha channel
                image[y_start + i, x_start + j] = (1 - alpha) * image[y_start + i, x_start + j] + alpha * emoji_resized[i, j, :3]

    def visualize_mask(self, image, detections, emoji_path, scale=1.0):
        """Visualize the pose with an emoji mask on specific landmarks."""
        pose_landmarks_list = detections.pose_landmarks
        annotated_image = np.copy(image)

        for pose_landmarks in pose_landmarks_list:
            # Add mask to the nose landmark as an example
            nose_landmark = pose_landmarks[self.NOSE_INDEX]
            self._add_mask(annotated_image, nose_landmark, emoji_path, scale)

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
    detector = PoseDetector()
    
    # Create a video capture object to read frames from the camera.
    cap = cv2.VideoCapture(0)

    # Process each frame.
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        detections = detector.detect(image)
        # image = detector.visualize(image, detections)
        image = detector.visualize_mask(image, detections, emoji_path="assets/smile.png", scale=4.0)

        # Display the annotated frame.
        cv2.imshow('MediaPipe Object Detection', image)

        if cv2.waitKey(5) & 0xFF == 27:  
            break
    
    # Release resources.
    cap.release()