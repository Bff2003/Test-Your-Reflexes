from src.detectors.HandsDetector import HandsDetector
import cv2

class HandsChallenges:

    LIST_CHALLENGES = []
    MIN_SCORE = 0.5

    def __init__(self, hands_detector: HandsDetector = None):
        if hands_detector is None:
            hands_detector = HandsDetector()
        self.hands_detector = hands_detector

    def is_v_gesture_in_frame(self, frame):
        detections = self.hands_detector.detect(frame)
        hand_landmarks = detections.hand_landmarks
        
        if hand_landmarks is None or len(hand_landmarks) == 0:
            return False

        for i in range(len(hand_landmarks)):
            hand = hand_landmarks[i]

            index_finger_up = hand[8].y < hand[6].y # indicador esticado para cima
            middle_finger_up = hand[12].y < hand[10].y # medio fechado para cima
            ring_finger_down = hand[14].y < hand[16].y # anelar fechado para baixo
            pinky_down = hand[18].y < hand[20].y # mindinho fechado para baixo

            spacing_between_index_and_middle_finger = abs(hand[8].x - hand[10].x) > 0.1 # espaco entre o indicador e o medio

            if index_finger_up and middle_finger_up and ring_finger_down and pinky_down and spacing_between_index_and_middle_finger:
                return True

        return False

    def is_closed_hand_gesture_in_frame(self, frame):
        # Detecta os landmarks das mãos no frame
        hand_landmarks = self.hands_detector.detect(frame).hand_landmarks
        
        if hand_landmarks is None or len(hand_landmarks) == 0:
            return False  # Retorna False se não houver landmarks detectados

        # Obter as coordenadas dos dedos
        for hand in hand_landmarks:
            # Obter as coordenadas dos dedos
            thumb_tip = hand[self.hands_detector.THUMB_TIP_INDEX]
            thumb_base = hand[self.hands_detector.THUMB_MCP_INDEX]
            
            index_finger_tip = hand[self.hands_detector.INDEX_FINGER_TIP_INDEX]
            middle_finger_tip = hand[self.hands_detector.MIDDLE_FINGER_TIP_INDEX]
            ring_finger_tip = hand[self.hands_detector.RING_FINGER_TIP_INDEX]
            pinky_tip = hand[self.hands_detector.PINKY_TIP_INDEX]

            # Verifica se o polegar está fechado (a ponta do polegar deve estar abaixo da base)
            thumb_closed = thumb_tip.y > thumb_base.y

            # Verifica se os dedos indicador, médio, anelar e mínimo estão fechados
            index_finger_closed = index_finger_tip.y > hand[self.hands_detector.INDEX_FINGER_MCP_INDEX].y
            middle_finger_closed = middle_finger_tip.y > hand[self.hands_detector.MIDDLE_FINGER_MCP_INDEX].y
            ring_finger_closed = ring_finger_tip.y > hand[self.hands_detector.RING_FINGER_MCP_INDEX].y
            pinky_closed = pinky_tip.y > hand[self.hands_detector.PINKY_MCP_INDEX].y

            # Retorna True se todos os dedos, exceto o polegar, estiverem fechados
            if (thumb_closed and 
                index_finger_closed and 
                middle_finger_closed and 
                ring_finger_closed and 
                pinky_closed):
                return True

        return False

    def is_l_gesture_in_frame(self, frame):
        detections = self.hands_detector.detect(frame)
        hand_landmarks = detections.hand_landmarks
        
        if hand_landmarks is None or len(hand_landmarks) == 0:
            return False

        for i in range(len(hand_landmarks)):
            hand = hand_landmarks[i]

            index_finger_up = hand[8].y < hand[6].y # indicador esticado para cima
            middle_finger_down = hand[10].y < hand[12].y # medio fechado para baixo
            ring_finger_down = hand[14].y < hand[16].y # anelar fechado para baixo
            pinky_down = hand[18].y < hand[20].y # mindinho fechado para baixo

            if detections.handedness[i][0].category_name == "Right":
                thumb_right = hand[4].x > hand[2].x # polegar esticado para a direita

                if index_finger_up and middle_finger_down and ring_finger_down and pinky_down and thumb_right:
                    return True
            
            elif detections.handedness[i][0].category_name == "Left":
                thumb_left = hand[4].x < hand[2].x # polegar esticado para a esquerda

                if index_finger_up and middle_finger_down and ring_finger_down and pinky_down and thumb_left:
                    return True

        return False

    def is_callme_gesture_in_frame(self, frame):
        detections = self.hands_detector.detect(frame)
        hand_landmarks = detections.hand_landmarks
        
        if hand_landmarks is None or len(hand_landmarks) == 0:
            return False

        for i in range(len(hand_landmarks)):
            hand = hand_landmarks[i]

            if detections.handedness[i][0].category_name == "Right":
                thumb_up = hand[self.hands_detector.THUMB_TIP_INDEX].y < hand[self.hands_detector.THUMB_MCP_INDEX].y # polegar esticado
                pinky_up = hand[20].x > hand[18].x # mindinho esticado
                index_down = hand[6].x > hand[8].x # indicador fechado
                middle_down = hand[10].x > hand[12].x # medio fechado
                ring_down = hand[14].x > hand[16].x # anelar fechado

                if (thumb_up and pinky_up and index_down and middle_down and ring_down):
                    return True

            elif detections.handedness[i][0].category_name == "Left":
                thumb_up = hand[self.hands_detector.THUMB_TIP_INDEX].y < hand[self.hands_detector.THUMB_MCP_INDEX].y # polegar esticado
                pinky_up = hand[20].x < hand[18].x # mindinho esticado
                index_down = hand[6].x < hand[8].x # indicador fechado
                middle_down = hand[10].x < hand[12].x # medio fechado
                ring_down = hand[14].x < hand[16].x # anelar fechado

                if (thumb_up and pinky_up and index_down and middle_down and ring_down):
                    return True

        return False

    def is_fixe_gesture_in_frame(self, frame):
        detections = self.hands_detector.detect(frame)
        hand_landmarks = detections.hand_landmarks
        tolerance = 0.07

        for i in range(len(hand_landmarks)):
            hand = hand_landmarks[i]
            if detections.handedness[i][0].category_name == "Right":
                thumb_up = hand[self.hands_detector.THUMB_TIP_INDEX].y < hand[self.hands_detector.THUMB_MCP_INDEX].y - tolerance
                index_finger_down = hand[8].x < hand[6].x + tolerance
                middle_finger_down = hand[12].x < hand[10].x + tolerance
                ring_finger_down = hand[16].x < hand[14].x + tolerance
                pinky_finger_down = hand[20].x < hand[18].x + tolerance

                thumb_distance = abs(hand[self.hands_detector.THUMB_TIP_INDEX].y - hand[self.hands_detector.THUMB_MCP_INDEX].y)
                thumb_distance = thumb_distance > 0.16
            
                if thumb_up and index_finger_down and middle_finger_down and ring_finger_down and pinky_finger_down and thumb_distance:
                    return True

            elif detections.handedness[i][0].category_name == "Left":
                thumb_up = hand[self.hands_detector.THUMB_TIP_INDEX].y < hand[self.hands_detector.THUMB_MCP_INDEX].y - tolerance
                index_finger_down = hand[8].x > hand[6].x - tolerance
                middle_finger_down = hand[12].x > hand[10].x - tolerance
                ring_finger_down = hand[16].x > hand[14].x - tolerance
                pinky_finger_down = hand[20].x > hand[18].x - tolerance

                thumb_distance = abs(hand[self.hands_detector.THUMB_TIP_INDEX].y - hand[self.hands_detector.THUMB_MCP_INDEX].y)
                thumb_distance = thumb_distance > 0.16
            
                if thumb_up and index_finger_down and middle_finger_down and ring_finger_down and pinky_finger_down and thumb_distance:
                    return True

        return False


if __name__ == "__main__":
    hands_detector = HandsDetector()
    hands_challenges = HandsChallenges(hands_detector)

    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        print(hands_challenges.is_fixe_gesture_in_frame(frame))

        detections = hands_detector.detect(frame)
        image = hands_detector.visualize(frame, detections)

        # Display the annotated frame.
        cv2.imshow('MediaPipe Object Detection', image)

        if cv2.waitKey(5) & 0xFF == 27:
            break

    # Release resources.
    cap.release()