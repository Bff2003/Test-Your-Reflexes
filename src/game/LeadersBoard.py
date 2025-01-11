from time import time
import json
import os
import cv2

class LeadersBoard:

    MAX_LEADERS = 3

    def __init__(self):
        self.__leaders = []
        self.__load_leaders()

    def reset_leaders(self):
        self.__leaders = []
        self.__save_leaders()
        return self.get_leaders()

    def __load_leaders(self):
        if not os.path.exists('assets'):
            os.makedirs('assets')
        if not os.path.exists('assets/leaders.json'):
            with open('assets/leaders.json', 'w') as file:
                json.dump([], file)
        else:
            with open('assets/leaders.json', 'r') as file:
                self.__leaders = json.load(file)
    
    def __save_leaders(self):
        with open('assets/leaders.json', 'w') as file:
            json.dump(self.__leaders, file, indent=4)
    
    def __duplicate_leader(self, name: str):
        for leader in self.__leaders:
            if leader[0] == name: 
                return leader 
        return False

    def add_leader(self, name: str, time: float, image = None):
        duplicate = self.__duplicate_leader(name)
        if duplicate != False and duplicate[1] <= time:
            return False
        
        if duplicate != False and duplicate[1] > time:
            duplicate[1] = time
            duplicate[2] = image
            self.__leaders = self.__order_leaders()
            self.__save_leaders()
            return self.get_leaders()

        self.__leaders.append((name, time, image))

        self.__leaders = self.__order_leaders()

        if len(self.__leaders) > self.MAX_LEADERS:
            self.__leaders.pop()
        
        self.__save_leaders()
        return self.get_leaders()

    def __order_leaders(self):
        self.__leaders.sort(key=lambda x: x[1])
        return self.get_leaders()
    
    def get_podium(self, number_of_leaders=3):
        return self.get_leaders()[0:number_of_leaders]

    def get_leaders(self):
        return self.__leaders.copy()
    
    def __str__(self):
        return str(self.__leaders)
    
    def draw_scores(self, frame, total_time, average_time):
        frame_height, frame_width, _ = frame.shape
        cv2.putText(frame, f"Total time: {total_time} seconds", (int(frame_width/2)-90, frame_height - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        cv2.putText(frame, f"Average time: {average_time} seconds", (int(frame_width/2)-90, frame_height - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        return frame

    def draw(self, frame, number_of_leaders=3):
        frame_height, frame_width, _ = frame.shape
        frame_width = frame_width - 10 # Remover margem
        frame_height = frame_height - 10 # Remover margem

        margin_between_squares = 10  # Margem horizontal entre os quadrados

        frame_width = frame_width - margin_between_squares * (number_of_leaders - 1)

        square_height = int(frame_height / number_of_leaders)
        square_width = int(frame_width / number_of_leaders)

        for i in range(len(self.get_podium(number_of_leaders))):
            leader = self.get_podium(number_of_leaders)[i]
            
            # Coordenadas do quadrado
            rect_x = i * (square_width + margin_between_squares) + margin_between_squares
            rect_y = int((frame_height - square_height) / 2)

            # Verificar se há imagem para o líder
            if leader[2] is not None and os.path.exists(leader[2]):
                image_path = leader[2]
                image = cv2.imread(image_path)

                if image is not None:
                    # Redimensionar a imagem para caber no quadrado
                    resized_image = cv2.resize(image, (square_width, square_height))
                    # Inserir a imagem no frame
                    frame[rect_y:rect_y + square_height, rect_x:rect_x + square_width] = resized_image
                else:
                    print(f"Erro ao carregar a imagem: {image_path}")
            else:
                # Desenhar o quadrado e colocar o nome dentro, se não houver imagem
                cv2.rectangle(frame, (rect_x, rect_y), (rect_x + square_width, rect_y + square_height), (255, 0, 0), 3)
                name_text = leader[0]
                name_size = cv2.getTextSize(name_text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
                name_x = rect_x + (square_width - name_size[0]) // 2
                name_y = rect_y + (square_height + name_size[1]) // 2
                cv2.putText(frame, name_text, (name_x, name_y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

            # Escrever a classificação acima do quadrado ou imagem
            classification_text = f"{i + 1} Lugar"
            text_size = cv2.getTextSize(classification_text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
            text_x = rect_x + (square_width - text_size[0]) // 2
            text_y = rect_y - 10
            cv2.putText(frame, classification_text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        return frame

        
if __name__ == '__main__':
    leaders = LeadersBoard()
    leaders.add_leader('A', 10)
    leaders.add_leader('A', 10)
    leaders.add_leader('B', 15)
    leaders.add_leader('C', 5)
    leaders.add_leader('D', 15)
    leaders.add_leader('E', 25)
    
    # Create a video capture object to read frames from the camera.
    cap = cv2.VideoCapture(0)

    # Process each frame.
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        detections = leaders.draw(image)
        # detections = leaders.draw_scores(image, 20, 20)

        # Display the annotated frame.
        cv2.imshow('MediaPipe Object Detection', image)

        if cv2.waitKey(5) & 0xFF == 27:  
            break
    
    # Release resources.
    cap.release()

    print(leaders)

