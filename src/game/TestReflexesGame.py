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

class TestReflexesGame:
    LEADERS_LIST = []

    def __pose_challenges():
        return [
            Challenge("Two hands up", PoseChallenges().is_two_hands_up_in_frame, Challenge.POSE, "assets/images/examples/pose/hands_up.png"),
            Challenge("Tilted to side Right or Left", PoseChallenges().is_tilted_to_side_in_frame, Challenge.POSE, "assets/images/examples/pose/tilted_to_side.jpg"),
            Challenge("Hand above head", PoseChallenges().is_hand_above_head_in_frame, Challenge.POSE, "assets/images/examples/pose/hand_above_head.jpg"),
            Challenge("T pose", PoseChallenges().is_t_pose_in_frame, Challenge.POSE, "assets/images/examples/pose/T.png"),
            Challenge("Turn head", PoseChallenges().is_turn_head_in_frame, Challenge.POSE, "assets/images/examples/pose/turn_head.jpg"),
            # Challenge("Tilt head", PoseChallenges().is_tilt_head_in_frame, Challenge.POSE, "assets/images/examples/pose/tilt_head.jpg"),
        ]

    def __object_challenges(allowed_objects = ["phone", "bottle", "cup", "backpack", "remote"]):
        to_return = []
        if "phone" in allowed_objects: to_return.append(Challenge("Phone in screen", ObjectsChallenges().is_phone_in_frame, Challenge.OBJECT, "assets/images/examples/objects/phone.png"))
        if "bottle" in allowed_objects: to_return.append(Challenge("Cup in screen", ObjectsChallenges().is_cup_in_frame, Challenge.OBJECT))
        if "cup" in allowed_objects: to_return.append(Challenge("Backpack in screen", ObjectsChallenges().is_backpack_in_frame, Challenge.OBJECT))
        if "remote" in allowed_objects: to_return.append(Challenge("Remote in screen", ObjectsChallenges().is_remote_in_frame, Challenge.OBJECT))
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

    def __init__(self, name):
        self.name = name if name else input("Enter your name: ")
        self.cap = cv2.VideoCapture(0)  # Inicializa a captura de vídeo
        self.running = True
        self.last_frame = None
        self.leaders_board = LeadersBoard()
        self.actual_challenge = None

        self.challenges_allowed = []
        self.challenges_allowed = self.challenges_allowed + TestReflexesGame.__hands_challenges()
        self.challenges_allowed = self.challenges_allowed + TestReflexesGame.__pose_challenges()
        self.challenges_allowed = self.challenges_allowed + TestReflexesGame.__object_challenges(allowed_objects=["phone"])

    def capture_video(self):
        while self.running:
            success, frame = self.cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue
            
            # Armazena o último frame capturado
            self.last_frame = frame.copy()

            self.drawable_frame = cv2.flip(self.last_frame, 1)

            try:
                if self.actual_challenge is not None:
                    if self.actual_challenge.image is not None and self.actual_challenge is not None:
                        id = IndicationDrawable(100, 20)
                        self.drawable_frame = id.draw(self.drawable_frame, cv2.imread(self.actual_challenge.image), ["Type:" + str(self.actual_challenge.challenge_type),"Do the challenge:", self.actual_challenge.name], (120, 120))
            except AttributeError:
                pass
            
            # Aqui você pode adicionar a lógica para mostrar o frame ou processá-lo
            cv2.imshow('Video Feed', self.drawable_frame)

            # Espera por uma tecla para fechar a janela
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.running = False
    
    def traffic_light(self):
        for i in range(3, 0, -1):
            print(f"{i}...")
            time.sleep(random.uniform(0.5, 1.5))
        print("Go!")

    def start_game(self):
        try:
            # Inicia a thread para capturar vídeo
            video_thread = Thread(target=self.capture_video)
            video_thread.start()

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
                    
                    self.actual_challenge = None
                    print("Movement valid!")
                    break

                end_time = time.time()
                movements_times.append([start_time, end_time])

                print(f"Mini game {i + 1} finished!")
            
            print("Game finished!")
            self.leaders_board.add_leader(self.name, sum([end_time - start_time for start_time, end_time in movements_times]))
            print("Time for each movement:")
            for i in range(len(movements_times)):
                print(f"Movement {i + 1}: {movements_times[i][1] - movements_times[i][0]} seconds")
            print(f"Total time: {sum([end_time - start_time for start_time, end_time in movements_times])} seconds")
            print(f"Average time: {sum([end_time - start_time for start_time, end_time in movements_times]) / len(movements_times)} seconds")

        finally:
            self.running = False  # Para a captura de vídeo
            video_thread.join()  # Espera a thread de vídeo terminar
            self.cap.release()  # Libera a captura de vídeo
            cv2.destroyAllWindows()  # Fecha todas as janelas
            print("Game finished!")


if __name__ == "__main__":
    game = TestReflexesGame(input("Enter your name: "))
    game.start_game()