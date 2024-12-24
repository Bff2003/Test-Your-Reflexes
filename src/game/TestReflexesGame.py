import time
import random
import cv2
from threading import Thread
from src.game.LeadersBoard import LeadersBoard
from src.game.Challenge import Challenge
from src.challenges.HandsChallenges import HandsChallenges
from src.challenges.ObjectsChallenges import ObjectsChallenges

class TestReflexesGame:
    LEADERS_LIST = []
    MOVEMENTS_LIST = [
        Challenge("Soco", HandsChallenges().is_closed_hand_gesture_in_frame, Challenge.HANDS),
        # Challenge("L", HandsChallenges().is_l_gesture_in_frame, Challenge.HANDS),
        Challenge("Call me", HandsChallenges().is_callme_gesture_in_frame, Challenge.HANDS),
        # Challenge("V", HandsChallenges().is_v_gesture_in_frame, Challenge.HANDS),
        Challenge("Fixe", HandsChallenges().is_fixe_gesture_in_frame, Challenge.HANDS),

        Challenge("Phone in screen", ObjectsChallenges().is_phone_in_frame, Challenge.OBJECT),
    ]

    def __init__(self, name):
        self.name = name if name else input("Enter your name: ")
        self.cap = cv2.VideoCapture(0)  # Inicializa a captura de vídeo
        self.running = True
        self.last_frame = None
        self.leaders_board = LeadersBoard()

    def capture_video(self):
        while self.running:
            success, frame = self.cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue
            
            # Armazena o último frame capturado
            self.last_frame = frame.copy()

            # Aqui você pode adicionar a lógica para mostrar o frame ou processá-lo
            frame = cv2.flip(frame, 1)
            cv2.imshow('Video Feed', frame)

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
            for i in range(5):  # Exemplo de 5 movimentos
                movement_choosed = random.randint(0, len(self.MOVEMENTS_LIST) - 1)

                # input("Press enter to simulate the movement")
                self.traffic_light()
                print(f"Movement chosen: {self.MOVEMENTS_LIST[movement_choosed].name}")
                start_time = time.time()
                while True:
                    # Passa o frame atual para is_valid()
                    if self.last_frame is None:
                        continue
                    if not self.MOVEMENTS_LIST[movement_choosed].is_valid(self.last_frame):  # Se o movimento não for válido
                        # print("Movement not valid!")
                        continue
                    
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