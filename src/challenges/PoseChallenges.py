from src.detectors.PoseDetector import PoseDetector
import cv2
import math
from icecream import ic

class PoseChallenges: # TODO Implement this class
    LIST_CHALLENGES = []
    MIN_SCORE = 0.5

    def __init__(self, pose_detector: PoseDetector = None):
        if pose_detector is None:
            pose_detector = PoseDetector()
        self.pose_detector = pose_detector

    def is_hand_above_head_in_frame(self, frame, detections = None):
        if detections is None:
            detections = self.pose_detector.detect(frame)
        for detection in detections.pose_landmarks:
            left_hand_up = detection[20].y < detection[0].y
            left_hand_nose_distance = abs(detection[20].y - detection[0].y) > 0.2

            right_hand_up = detection[19].y < detection[0].y
            right_hand_nose_distance = abs(detection[19].y - detection[0].y) > 0.2
            return (left_hand_up and left_hand_nose_distance) or (right_hand_up and right_hand_nose_distance)
        return False

    def is_two_hands_up_in_frame(self, frame, detections = None):
        if detections is None:
            detections = self.pose_detector.detect(frame)
        for detection in detections.pose_landmarks:
            right_hand_up = detection[16].y < detection[8].y
            left_hand_up = detection[15].y < detection[9].y
            return left_hand_up and right_hand_up
        return False

    def is_tilted_to_side_in_frame(self, frame, threshold = 0.02, detections = None):
        """ Cabeça inclinada para a esquerda ou para a direita"""
        if detections is None:
            detections = self.pose_detector.detect(frame)
        for detection in detections.pose_landmarks:
            eye_diff = abs(detection[1].y - detection[3].y)
            if eye_diff > threshold: # se houver uma diferenca grande entre os olhos no eixo y
                return True
        return False

    def is_t_pose_in_frame(self, frame, threshold = 0.1, detections = None):
        """ Braços esticados """
        if detections is None:
            detections = self.pose_detector.detect(frame)
        for detection in detections.pose_landmarks:
            right_arm = abs(detection[11].y - detection[13].y)
            left_arm = abs(detection[12].y - detection[14].y)

            if right_arm < threshold and left_arm < threshold:
                return True
        return False
    
    def is_turn_head_in_frame(self, frame, threshold = 0.07, detections = None):
        """ Cabeça virada para a esquerda ou direita """
        if detections is None:
            detections = self.pose_detector.detect(frame)
        for detection in detections.pose_landmarks:
            end_face = abs(detection[7].x - detection[8].x)

            if end_face < threshold:
                return True
        return False
    
    def is_left_hand_in_right_shoulder(self, frame, detections = None):
        if detections is None:
            detections = self.pose_detector.detect(frame)
        for detection in detections.pose_landmarks:
            index_left_hand = 19
            index_right_shoulder = 12

            left_hand = detection[index_left_hand]
            right_shoulder = detection[index_right_shoulder]
            
            if math.dist((left_hand.x, left_hand.y), (right_shoulder.x, right_shoulder.y)) < 0.1:
                return True
        return False

    def is_right_hand_in_left_shoulder(self, frame, detections = None):
        if detections is None:
            detections = self.pose_detector.detect(frame)
        for detection in detections.pose_landmarks:
            index_right_hand = 20
            index_left_shoulder = 11

            right_hand = detection[index_right_hand]
            left_shoulder = detection[index_left_shoulder]
            
            if math.dist((right_hand.x, right_hand.y), (left_shoulder.x, left_shoulder.y)) < 0.1:
                return True
        return False

if __name__ == "__main__":
    pose_detector = PoseDetector()
    pose_challenges = PoseChallenges(pose_detector)

    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        detections = pose_detector.detect(frame)
        image = pose_detector.visualize(frame, detections)

        a = pose_challenges.is_left_hand_in_right_shoulder(frame)
        print(a)
        # if a == True:
        #     break
        # print(pose_challenges.is_tilt_head_in_frame(frame))

        # Display the annotated frame.
        cv2.imshow('MediaPipe Object Detection', image)

        if cv2.waitKey(5) & 0xFF == 27:
            break
            
    # Release resources.
    cap.release()


    

    