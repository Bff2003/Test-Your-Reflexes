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
        # Detecta os landmarks das mãos no frame
        hand_landmarks = self.hands_detector.detect(frame).hand_landmarks
        
        if hand_landmarks is None or len(hand_landmarks) == 0:
            return False  # Retorna False se não houver landmarks detectados

        # Obter as coordenadas dos dedos
        for hand in hand_landmarks:
            index_finger_tip = hand[self.hands_detector.INDEX_FINGER_TIP_INDEX]
            index_finger_base = hand[self.hands_detector.INDEX_FINGER_MCP_INDEX]
            
            middle_finger_tip = hand[self.hands_detector.MIDDLE_FINGER_TIP_INDEX]
            middle_finger_base = hand[self.hands_detector.MIDDLE_FINGER_MCP_INDEX]

            pinky_tip = hand[self.hands_detector.PINKY_TIP_INDEX]
            ring_finger_tip = hand[self.hands_detector.RING_FINGER_TIP_INDEX]
            thumb_tip = hand[self.hands_detector.THUMB_TIP_INDEX]

            # Verifica se os dedos indicador e do meio estão esticados
            index_finger_straight = index_finger_tip.y < index_finger_base.y
            middle_finger_straight = middle_finger_tip.y < middle_finger_base.y

            # Verifica se os dedos mínimo, anelar e polegar estão fechados
            pinky_closed = pinky_tip.y > hand[self.hands_detector.PINKY_MCP_INDEX].y
            ring_finger_closed = ring_finger_tip.y > hand[self.hands_detector.RING_FINGER_MCP_INDEX].y
            thumb_closed = thumb_tip.y > hand[self.hands_detector.THUMB_MCP_INDEX].y

            # Verifica se os dedos estão separados (usando a distância entre as pontas dos dedos)
            distance_between_fingers = abs(index_finger_tip.x - middle_finger_tip.x)
            
            # Define um limite para considerar que os dedos estão separados
            separation_threshold = 0.1  # Ajuste conforme necessário

            # Retorna True se os dedos indicador e do meio estiverem esticados e separados,
            # e os dedos mínimo, anelar e polegar estiverem fechados
            return (index_finger_straight and 
                    middle_finger_straight and 
                    distance_between_fingers > separation_threshold and 
                    pinky_closed and 
                    ring_finger_closed and 
                    thumb_closed)

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
            index_finger_base = hand[self.hands_detector.INDEX_FINGER_MCP_INDEX]
            
            middle_finger_tip = hand[self.hands_detector.MIDDLE_FINGER_TIP_INDEX]
            ring_finger_tip = hand[self.hands_detector.RING_FINGER_TIP_INDEX]
            pinky_tip = hand[self.hands_detector.PINKY_TIP_INDEX]

            # Verifica se o polegar está esticado para o lado
            thumb_straight = thumb_tip.x > thumb_base.x and thumb_tip.y < thumb_base.y

            # Verifica se o dedo indicador está esticado
            index_finger_straight = index_finger_tip.y < index_finger_base.y

            # Verifica se os dedos médio, anelar e mínimo estão fechados
            middle_finger_closed = middle_finger_tip.y > hand[self.hands_detector.MIDDLE_FINGER_MCP_INDEX].y
            ring_finger_closed = ring_finger_tip.y > hand[self.hands_detector.RING_FINGER_MCP_INDEX].y
            pinky_closed = pinky_tip.y > hand[self.hands_detector.PINKY_MCP_INDEX].y

            # Retorna True se o gesto "L" estiver presente
            if (thumb_straight and 
                index_finger_straight and 
                middle_finger_closed and 
                ring_finger_closed and 
                pinky_closed):
                return True

        return False

    
    # V
    # SOCO
    # L
    # Liga-me
    # Fixe

if __name__ == "__main__":
    hands_detector = HandsDetector()
    hands_challenges = HandsChallenges(hands_detector)

    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        print(hands_challenges.is_l_gesture_in_frame(frame))

        detections = hands_detector.detect(frame)
        image = hands_detector.visualize(frame, detections)


        # Display the annotated frame.
        cv2.imshow('MediaPipe Object Detection', image)

        if cv2.waitKey(5) & 0xFF == 27:
            break

    # Release resources.
    cap.release()


    

    