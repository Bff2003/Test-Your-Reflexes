import time
import random
import cv2
from threading import Thread
from src.game.LeadersBoard import LeadersBoard
from src.game.Challenge import Challenge
from src.challenges.HandsChallenges import HandsChallenges
from src.challenges.ObjectsChallenges import ObjectsChallenges
from src.challenges.PoseChallenges import PoseChallenges
from src.game.drawables.IndicationDrawable  import IndicationDrawable
from src.game.drawables.TrafficLightDrawable import TrafficLightDrawable
from src.detectors.FaceDetector import FaceDetector
from src.detectors.PoseDetector import PoseDetector
from src.game.ScreenRecorder import ScreenRecorder
import pygame
import os

class TestReflexesGame:
    LEADERS_LIST = []

    SCREEN_LEADERS = 0
    SCREEN_CHALLENGES = 1
    SCREEN_MASK = 2

    SUCESS_SOUND = "assets/sounds/success.mp3"
    VICTORY_SOUND = "assets/sounds/victory.mp3"

    def __pose_challenges():
        return [
            Challenge("Two hands up", PoseChallenges().is_two_hands_up_in_frame, Challenge.POSE, "assets/images/examples/pose/hands_up.png"),
            Challenge("Tilted to side Right or Left", PoseChallenges().is_tilted_to_side_in_frame, Challenge.POSE, "assets/images/examples/pose/tilted_to_side.jpg"),
            Challenge("Hand above head", PoseChallenges().is_hand_above_head_in_frame, Challenge.POSE, "assets/images/examples/pose/hand_above_head.jpg"),
            Challenge("T pose", PoseChallenges().is_t_pose_in_frame, Challenge.POSE, "assets/images/examples/pose/T.png"),
            Challenge("Turn head", PoseChallenges().is_turn_head_in_frame, Challenge.POSE, "assets/images/examples/pose/turn_head.jpg"),
            Challenge("Left hand on right shoulder", PoseChallenges().is_left_hand_in_right_shoulder, Challenge.POSE, "assets/images/examples/pose/left_hand_in_right_shoulder.png"),
            Challenge("Right hand on left shoulder", PoseChallenges().is_right_hand_in_left_shoulder, Challenge.POSE, "assets/images/examples/pose/right_hand_in_left_shoulder.png"),
        ]

    def __object_challenges(allowed_objects = ["phone", "bottle", "cup", "backpack", "remote"]):
        to_return = []
        if "phone" in allowed_objects: to_return.append(Challenge("Phone in screen", ObjectsChallenges().is_phone_in_frame, Challenge.OBJECT, "assets/images/examples/objects/phone.png"))
        if "cup" in allowed_objects: to_return.append(Challenge("Cup in screen", ObjectsChallenges().is_cup_in_frame, Challenge.OBJECT, "assets/images/examples/objects/cup.png"))
        if "backpack" in allowed_objects: to_return.append(Challenge("Backpack in screen", ObjectsChallenges().is_backpack_in_frame, Challenge.OBJECT, "assets/images/examples/objects/backpack.png"))
        if "bottle" in allowed_objects: to_return.append(Challenge("Bottle in screen", ObjectsChallenges().is_bottle_in_frame, Challenge.OBJECT, "assets/images/examples/objects/bottle.png"))
        if "remote" in allowed_objects: to_return.append(Challenge("Remote in screen", ObjectsChallenges().is_remote_in_frame, Challenge.OBJECT, "assets/images/examples/objects/remote.png"))
        return to_return

    def __hands_challenges():
        return [
            Challenge("Soco", HandsChallenges().is_closed_hand_gesture_in_frame, Challenge.HANDS, "assets/images/examples/hands/soco.png"),
            Challenge("L", HandsChallenges().is_l_gesture_in_frame, Challenge.HANDS, "assets/images/examples/hands/L.png"),
            Challenge("Call me", HandsChallenges().is_callme_gesture_in_frame, Challenge.HANDS, "assets/images/examples/hands/callme.png"),
            Challenge("V", HandsChallenges().is_v_gesture_in_frame, Challenge.HANDS, "assets/images/examples/hands/v.png"),
            Challenge("Fixe", HandsChallenges().is_fixe_gesture_in_frame, Challenge.HANDS, "assets/images/examples/hands/fixe.png")
        ]

    def __ask(title, options: list, default: int, repeat_title = True, pre_ask: str = None):
        i = 0
        print(title)
        while True:
            if i != 0 and repeat_title == True:
                print(title)
            
            for k in range(len(options)):
                print(f"\t{k+1} - {options[k]}")
            
            ask = "Choose: "
            if (pre_ask != None):
                ask = pre_ask
            
            response = input(ask)

            choosed = int(response)-1
            if (choosed >= 0 and choosed <= len(options)-1):
                return choosed
            
            i=i+1

    def __init__(self, name = None, user_image = None):  
        self.name = name if name else input("Enter your name: ")
        self.user_image = user_image if user_image else input("Enter your image path: ")
        if not os.path.exists(self.user_image):
            self.user_image = None
        self.cap = cv2.VideoCapture(0)  # Inicializa a captura de vídeo
        self.running = True
        self.last_frame = None
        self.leaders_board = LeadersBoard()
        self.actual_challenge = None
        self.traffic_light_drawable = TrafficLightDrawable()
        self.current_screen = TestReflexesGame.SCREEN_LEADERS
        self.face_detector = FaceDetector()
        self.pose_detector = PoseDetector()
        self.screen_recorder = ScreenRecorder()
        self.last_score = None

        self.challenges_allowed = []
        self.challenges_allowed = self.challenges_allowed + TestReflexesGame.__hands_challenges()
        self.challenges_allowed = self.challenges_allowed + TestReflexesGame.__pose_challenges()
        self.challenges_allowed = self.challenges_allowed + TestReflexesGame.__object_challenges(allowed_objects=["phone"])

    def capture_video(self):
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        while self.running:
            success, frame = self.cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue
            
            frame_height, frame_width, _ = frame.shape

            self.last_frame = frame.copy()

            self.drawable_frame = cv2.flip(self.last_frame, 1)

            if self.current_screen == TestReflexesGame.SCREEN_LEADERS:
                self.drawable_frame = self.leaders_board.draw(self.drawable_frame)
                cv2.putText(self.drawable_frame, f"Recording: {self.screen_recorder.is_recording()}", (int(frame_width/2)-90, frame_height - 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                cv2.putText(self.drawable_frame, "Press SPACE to start the game", (int(frame_width/2)-90, frame_height - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                cv2.putText(self.drawable_frame, "Press R to start recording", (int(frame_width/2)-90, frame_height - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            if self.current_screen == TestReflexesGame.SCREEN_CHALLENGES:
                self.drawable_frame = self.traffic_light_drawable.draw(self.drawable_frame, margin=(10, 100))
                try:
                    if self.actual_challenge is not None:
                        if self.actual_challenge.image is not None and self.actual_challenge is not None:
                            id = IndicationDrawable(100, 20)
                            self.drawable_frame = id.draw(self.drawable_frame, cv2.imread(self.actual_challenge.image), ["Type: " + Challenge.LIST_CHALLENGES_TYPES_STR[self.actual_challenge.challenge_type].capitalize(),"Do the challenge:", self.actual_challenge.name], (120, 120))
                except AttributeError:
                    pass

            if self.current_screen == TestReflexesGame.SCREEN_MASK and self.last_score is not None:
                self.drawable_frame = self.leaders_board.draw_scores(self.drawable_frame, self.last_score["total"], self.last_score["average"])
                detections = self.pose_detector.detect(self.drawable_frame)
                self.drawable_frame = self.pose_detector.visualize_mask(self.drawable_frame, detections, 'assets/smile.png')

            cv2.imshow('Video Feed', self.drawable_frame)

            self.screen_recorder.record_frame(self.drawable_frame)

            key = cv2.waitKey(1)
            if key & 0xFF == ord('q'):
                self.running = False
            elif key & 0xFF == ord('r'):
                if (self.screen_recorder.is_recording()): self.screen_recorder.stop_recording()
                else: self.screen_recorder.start_recording(self.drawable_frame)
            elif key & 0xFF == 32 and self.current_screen == TestReflexesGame.SCREEN_LEADERS:
                self.current_screen = TestReflexesGame.SCREEN_CHALLENGES
    
    def traffic_light(self):
        for i in range(3, 0, -1):
            print(f"{i}...")
            if i == 3:
                self.traffic_light_drawable.set_state(TrafficLightDrawable.STATE.RED)
            elif i == 2:
                self.traffic_light_drawable.set_state(TrafficLightDrawable.STATE.YELLOW)
            elif i == 1:
                self.traffic_light_drawable.set_state(TrafficLightDrawable.STATE.GREEN)

            time.sleep(random.uniform(0.5, 1.5))
            self.traffic_light_drawable.set_state(TrafficLightDrawable.STATE.ALL_GREEN)
        print("Go!")

    def start_game(self):
        try:
            pygame.init()
            # Inicia a thread para capturar vídeo
            video_thread = Thread(target=self.capture_video)
            video_thread.start()

            self.current_screen = TestReflexesGame.SCREEN_LEADERS

            if self.current_screen == TestReflexesGame.SCREEN_LEADERS:
                print("Press to SPACE to start the game")

            while True:
                if self.current_screen == TestReflexesGame.SCREEN_CHALLENGES:
                    break

            if self.current_screen == TestReflexesGame.SCREEN_CHALLENGES:
                movements_times = []
                last_movement = -1
                for i in range(5):  # Exemplo de 5 movimentos
                    while True:
                        movement_choosed = random.randint(0, len(self.challenges_allowed) - 1)
                        if (movement_choosed != last_movement):
                            break
                    
                    # input("Press enter to simulate the movement")
                    self.traffic_light()
                    print(f"Movement chosen: {self.challenges_allowed[movement_choosed].name}")
                    start_time = time.time()
                    while True:
                        # Passa o frame atual para is_valid()
                        if self.last_frame is None:
                            continue

                        self.actual_challenge = self.challenges_allowed[movement_choosed]
                        
                        if not self.challenges_allowed[movement_choosed].is_valid(self.last_frame):  # Se o movimento não for válido
                            # print("Movement not valid!")
                            continue

                        if time.time() - start_time > 0.55:
                            self.actual_challenge = None
                            print("Movement valid!")
                            pygame.mixer.Sound(TestReflexesGame.SUCESS_SOUND).play()
                            break

                    end_time = time.time()
                    movements_times.append([start_time, end_time])

                    print(f"Mini game {i + 1} finished!")
                
                print("Game finished!")
                self.leaders_board.add_leader(self.name, sum([end_time - start_time for start_time, end_time in movements_times]), self.user_image)
                print("Time for each movement:")
                for i in range(len(movements_times)):
                    print(f"Movement {i + 1}: {movements_times[i][1] - movements_times[i][0]} seconds")
                print(f"Total time: {sum([end_time - start_time for start_time, end_time in movements_times])} seconds")
                print(f"Average time: {sum([end_time - start_time for start_time, end_time in movements_times]) / len(movements_times)} seconds")

                self.last_score = {
                    "total": round(sum([end_time - start_time for start_time, end_time in movements_times]), 2),
                    "average": round(sum([end_time - start_time for start_time, end_time in movements_times]) / len(movements_times), 2),
                    "movements": movements_times
                }

                time.sleep(0.5)
                self.current_screen = TestReflexesGame.SCREEN_MASK

            if self.current_screen == TestReflexesGame.SCREEN_MASK:
                pygame.mixer.Sound(TestReflexesGame.VICTORY_SOUND).play()
                time.sleep(7)

        finally:
            self.screen_recorder.stop_recording()
            self.running = False  # Para a captura de vídeo
            video_thread.join()  # Espera a thread de vídeo terminar
            self.cap.release()  # Libera a captura de vídeo
            cv2.destroyAllWindows()  # Fecha todas as janelas
            print("Game finished!")


if __name__ == "__main__":
    game = TestReflexesGame(input("Enter your name: "))
    game.start_game()