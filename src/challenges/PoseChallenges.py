from src.detectors.PoseDetector import PoseDetector
import cv2

class PoseChallenges: # TODO Implement this class
    LIST_CHALLENGES = []
    MIN_SCORE = 0.5

    def __init__(self, pose_detector: PoseDetector = None):
        if pose_detector is None:
            pose_detector = PoseDetector()
        self.pose_detector = pose_detector

    def is_hand_above_head_in_frame(self, frame):
        detections = self.pose_detector.detect(frame)
        for detection in detections.pose_landmarks:
            left_hand_up = detection[20].y < detection[0].y
            left_hand_nose_distance = abs(detection[20].y - detection[0].y) > 0.2

            right_hand_up = detection[19].y < detection[0].y
            right_hand_nose_distance = abs(detection[19].y - detection[0].y) > 0.2
            return (left_hand_up and left_hand_nose_distance) or (right_hand_up and right_hand_nose_distance)
        return False

    def is_two_hands_up_in_frame(self, frame):
        detections = self.pose_detector.detect(frame)
        for detection in detections.pose_landmarks:
            right_hand_up = detection[16].y < detection[8].y
            left_hand_up = detection[15].y < detection[9].y
            return left_hand_up and right_hand_up
        return False

    def is_tilted_to_side_in_frame(self, frame, threshold = 0.02):
        """ Cabeça inclinada para a esquerda ou para a direita"""
        detections = self.pose_detector.detect(frame)
        for detection in detections.pose_landmarks:
            eye_diff = abs(detection[1].y - detection[3].y)
            if eye_diff > threshold: # se houver uma diferenca grande entre os olhos no eixo y
                return True
        return False

    def is_t_pose_in_frame(self, frame): # TODO T Pose
        raise NotImplementedError
    
    def is_turn_head_in_frame(self, frame): # TODO Turn Head
        raise NotImplementedError
    
    def is_tilt_head_in_frame(self, frame): # TODO Tilt Head
        raise NotImplementedError

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

        print(pose_challenges.is_hand_above_head_in_frame(frame))
        # print(pose_challenges.is_tilt_head_in_frame(frame))

        # Display the annotated frame.
        cv2.imshow('MediaPipe Object Detection', image)

        if cv2.waitKey(5) & 0xFF == 27:
            break
            
    # Release resources.
    cap.release()


    

    