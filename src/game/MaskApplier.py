import cv2
import numpy as np
import mediapipe as mp
import src.Utils as Utils

class MaskApplier:
    def __init__(self, mask_path="assets/smile.png"):
        self.mask_path = mask_path
        self.mask_image = cv2.imread(mask_path, cv2.IMREAD_UNCHANGED)
        self.mp_pose = mp.solutions.pose

    def apply_mask(self, frame, detections, scale=3.5):
        if len(detections.pose_landmarks) == 0:
            return frame
        
        landmarks = detections.pose_landmarks[0]

        # Acesse os landmarks da primeira detecção
        nose = landmarks[self.mp_pose.PoseLandmark.NOSE.value]
        left_eye = landmarks[self.mp_pose.PoseLandmark.LEFT_EYE.value]
        right_eye = landmarks[self.mp_pose.PoseLandmark.RIGHT_EYE.value]

        eye_distance = np.linalg.norm(np.array([left_eye.x, left_eye.y]) - np.array([right_eye.x, right_eye.y]))

        mask_width = int(eye_distance * frame.shape[1] * scale)  # Ajuste a escala conforme necessário
        mask_height = int((mask_width * self.mask_image.shape[0] / self.mask_image.shape[1])) # Mantém a proporção

        resized_mask = cv2.resize(self.mask_image, (mask_width, mask_height), interpolation=cv2.INTER_AREA)

        x = int((left_eye.x + right_eye.x) / 2 * frame.shape[1]) - resized_mask.shape[1] // 2
        y = int(nose.y * frame.shape[0]) - resized_mask.shape[0] // 2

        if x < 0 or y < 0 or x + resized_mask.shape[1] > frame.shape[1] or y + resized_mask.shape[0] > frame.shape[0]:
            print("Máscara fora dos limites da imagem")
            return frame

        frame = Utils.overlay_image(frame, resized_mask, (x, y))
        return frame

if __name__ == "__main__":
    from src.detectors.PoseDetector import PoseDetector
    pose_detector = PoseDetector()
    mask_applier = MaskApplier()

    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue
    
        detections = pose_detector.detect(frame)
        frame = mask_applier.apply_mask(frame, detections)
        cv2.imshow('Video Feed', frame)
        cv2.waitKey(1)
